#!/usr/bin/env python3
"""Import posts from the existing niks-website Jekyll checkout, read-only."""

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]


def digest(content):
    return hashlib.sha256(content).hexdigest()


def import_posts(source, destination=ROOT):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    config_path = source / "_config.yml"
    config = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    origin = re.search(r'''(?m)^url:\s*["']?(https?://[^\s"'#]+)''', config)
    source_origin = origin[1].rstrip("/") if origin else "https://novarac.com"
    records = []
    for path in sorted((source / "_posts").glob("*.md")):
        filename = re.fullmatch(r"(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md", path.name)
        if not filename:
            raise ValueError(f"Unsupported Jekyll filename: {path.name}")
        published, slug = date.fromisoformat(filename[1]), filename[2]
        raw = path.read_bytes()
        text = raw.decode("utf-8").replace("\r\n", "\n")
        front = re.fullmatch(r"---\n(.*?)\n---\n(.*)", text, re.S)
        if not front:
            raise ValueError(f"Missing front matter: {path.name}")
        meta = {}
        for line in front[1].splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            key, separator, value = line.partition(":")
            if not separator or key.strip() in meta:
                raise ValueError(f"Unsupported front matter in {path.name}")
            meta[key.strip()] = value.strip()
        if set(meta) - {"layout", "title", "category", "description"}:
            raise ValueError(f"Unexpected metadata in {path.name}; review before importing")
        for key in ("title", "description", "category"):
            if not meta.get(key):
                raise ValueError(f"Missing {key}: {path.name}")
        category = meta["category"]
        # The source has no permalink override. Jekyll's default date style
        # includes the singular category as one path segment, including spaces.
        dated_path = f"/{quote(category.lower(), safe='&')}/{published:%Y/%m/%d}/{slug}.html"
        records.append({"path": path, "raw": raw, "meta": meta, "body": front[2],
                        "date": published.isoformat(), "slug": slug,
                        "canonical_path": f"/blog/{slug}/",
                        "legacy_paths": [f"/{slug}/", dated_path]})
    if not records:
        raise ValueError("No Markdown posts found in the source _posts directory")

    legacy = {path: record["canonical_path"] for record in records for path in record["legacy_paths"]}
    writes = {}
    assets = {}
    posts = []
    for record in records:
        used_images = []

        def image(match):
            filename = match[1]
            if Path(filename).name != filename:
                raise ValueError(f"Unsupported image path: {filename}")
            original = source / "assets" / "img" / filename
            content = original.read_bytes()
            target = f"src/assets/img/{filename}"
            writes[target] = content
            assets[filename] = {"source_file": f"assets/img/{filename}", "target_file": target,
                                "sha256": digest(content)}
            used_images.append(f"/assets/img/{filename}")
            return f"../../assets/img/{filename}"

        body = re.sub(r"\{\{\s*site\.url\s*\}\}/assets/img/([^\s)]+)", image, record["body"])
        if "{{" in body or "{%" in body:
            raise ValueError(f"Unresolved Liquid in {record['path'].name}")

        def internal_link(match):
            url = urlsplit(match[1])
            if url.hostname not in ("novarac.com", "www.novarac.com") or url.path not in legacy:
                return match[0]
            target = "../" + legacy[url.path].removeprefix("/blog/")
            return "](" + urlunsplit(("", "", target, url.query, url.fragment)) + ")"

        body = re.sub(r"\]\((https?://[^\s)]+)\)", internal_link, body)
        meta = record["meta"]
        header = (f"---\ntitle: {meta['title']}\ndate: {record['date']}\n"
                  f"description: {meta['description']}\ndraft: false\n---\n")
        target = f"content/posts/{record['slug']}.md"
        content = (header + body).encode("utf-8")
        writes[target] = content
        posts.append({"source_file": f"_posts/{record['path'].name}",
                      "source_sha256": digest(record["raw"]), "target_file": target,
                      "target_sha256": digest(content), "title": meta["title"],
                      "date": record["date"], "category": meta["category"],
                      "canonical_path": record["canonical_path"],
                      "feed_guid": source_origin + record["legacy_paths"][-1],
                      "legacy_paths": record["legacy_paths"], "images": used_images})

    for target, content in writes.items():
        path = destination / target
        if path.exists() and path.read_bytes() != content:
            raise ValueError(f"Existing content differs: {target}; preserve it and review manually")
    try:
        commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError:
        commit = None
    manifest = {"source_site": "https://novarac.com", "source_repository": source.name,
                "source_commit": commit, "posts": posts, "assets": list(assets.values()),
                "archive_aliases": {"/archive/": "/blog/", "/archive.html": "/blog/"}}
    for target, content in writes.items():
        path = destination / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    manifest_path = destination / "content" / "novarac-migration.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Imported {len(posts)} posts and {len(assets)} referenced images from {source.name}.")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Existing niks-website checkout")
    args = parser.parse_args()
    try:
        import_posts(args.source)
    except (ValueError, FileNotFoundError) as error:
        parser.exit(1, f"Import failed: {error}\n")
