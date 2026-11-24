#!/usr/bin/env python3
"""Build Nik’s static website. Python 3.9+, no third-party dependencies."""

import argparse
from datetime import date, datetime, timezone
from email.utils import format_datetime
from html import escape, unescape
import hashlib
import json
from pathlib import Path
import re
import shutil
from string import Template
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

from markdown import render
from gallery import dotted_screenshots

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
POSTS = ROOT / "content" / "posts"
MIGRATION = ROOT / "content" / "novarac-migration.json"
CONFIG = ROOT / "site.json"


def read_posts(include_drafts=False):
    posts = []
    for path in sorted(POSTS.glob("*.md")):
        slug = path.stem
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError(f"{path.name}: use a lowercase, hyphenated filename")
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)(.*)\Z", text, re.S)
        if not match:
            raise ValueError(f"{path.name}: missing front matter")
        meta = {}
        for line in match[1].splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            key, separator, value = line.partition(":")
            if not separator or key.strip() not in ("title", "date", "description", "draft"):
                raise ValueError(f"{path.name}: unsupported front matter line: {line}")
            key, value = key.strip(), value.strip()
            if key in meta:
                raise ValueError(f"{path.name}: duplicate {key}")
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            meta[key] = value
        for key in ("title", "date", "description"):
            if not meta.get(key):
                raise ValueError(f"{path.name}: {key} is required")
        if meta.get("draft", "true").lower() not in ("true", "false"):
            raise ValueError(f"{path.name}: draft must be true or false")
        published = date.fromisoformat(meta["date"])
        draft = meta.get("draft", "true").lower() == "true" or published > date.today()
        if draft and not include_drafts:
            continue
        body = render(match[2])
        words = len(re.findall(r"\b\w+\b", match[2]))
        posts.append({**meta, "slug": slug, "published": published, "draft": draft,
                      "body": body, "minutes": max(1, (words + 199) // 200)})
    return sorted(posts, key=lambda post: (post["published"], post["slug"]), reverse=True)


def pretty_date(value):
    return f"{value:%B} {value.day}, {value.year}"


def external_icon():
    return '<svg class="link-icon" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M7 5h8v8M15 5 5 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def configured_app_url(config, key):
    value = config.get("apps", {}).get("dotted", {}).get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Dotted Line {key} must be a full HTTP(S) URL or null")
    value = value.strip()
    if not value:
        return None
    parsed = urlsplit(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"Dotted Line {key} must be a full HTTP(S) URL or null")
    return value


def app_card(root="./"):
    url = escape(f"{root}apps/dotted/", quote=True)
    return f'''<a class="app-card" href="{url}"><img class="app-icon" src="{root}assets/dotted-icon.png" width="64" height="64" alt=""><div class="app-card-copy"><h3>Dotted Line</h3><p>Visualize your day, week, month, and year in dots.</p><span class="platforms">iPhone, iPad, and Mac</span></div></a>'''


def post_list(posts, root="./", limit=None, compact=False):
    shown = posts[:limit] if limit else posts
    if not shown:
        return '<div class="writing-empty"><h3>No posts yet.</h3><p>New posts will appear here.</p></div>'
    rows = []
    for post in shown:
        draft = '<span class="draft-label">Draft preview</span>' if post["draft"] else ""
        if compact:
            rows.append(f'''<a class="post-row post-row--compact" href="{root}blog/{post['slug']}/"><time class="post-meta" datetime="{post['published'].isoformat()}">{pretty_date(post['published'])}</time><div class="post-summary"><h3>{escape(post['title'])}{(' ' + draft) if draft else ''}</h3></div></a>''')
            continue
        rows.append(f'''<a class="post-row" href="{root}blog/{post['slug']}/"><div class="post-meta"><time datetime="{post['published'].isoformat()}">{pretty_date(post['published'])}</time><span>{post['minutes']} min read {draft}</span></div><div class="post-summary"><h3>{escape(post['title'])}</h3><p>{escape(post['description'])}</p></div></a>''')
    return "".join(rows)


def home(posts, person_name):
    return f'''<section class="hero"><div class="hero-copy"><h1>Hi, I’m {escape(person_name)}.</h1><p class="hero-role">Software engineer, data scientist, and independent app developer.</p><p class="hero-intro">I’ve spent 10 years building software and 5+ years working in data science. Here you’ll find what I’m currently working on and my thoughts on different subjects.</p></div></section>
    <section class="home-section"><div class="section-heading"><h2>Apps</h2><a class="plain-link" href="./apps/">All apps</a></div><div class="app-list">{app_card()}</div></section>
    <section class="home-section writing-section"><div class="section-heading"><h2>Recent posts</h2><a class="plain-link" href="./blog/">All posts</a></div><div class="post-list">{post_list(posts, limit=3, compact=True)}</div></section>'''


def apps():
    return f'''<section class="page-intro"><h1>Apps</h1><p>Here is the software I’ve built.</p></section><section class="app-catalog app-list" aria-label="Apps">{app_card('../')}</section><p class="page-note">Questions or feedback? <a href="mailto:{{email}}">Email me.</a></p>'''


def dotted(website_url=None, app_store_url=None):
    links = []
    if website_url:
        links.append(f'<a class="button product-website" href="{escape(website_url, quote=True)}">Visit Dotted Line’s website {external_icon()}</a>')
    if app_store_url:
        links.append(f'<a class="button button-secondary" href="{escape(app_store_url, quote=True)}">View on the App Store {external_icon()}</a>')
    actions = '<div class="product-actions">' + ''.join(links) + '</div>' if links else ''
    gallery = dotted_screenshots()
    return f'''<a class="back-link" href="../">Back to apps</a><section class="product-hero"><div class="product-title"><img class="app-icon" src="../../assets/dotted-icon.png" width="80" height="80" alt=""><div><h1>Dotted Line</h1><p class="platforms">iPhone, iPad, and Mac</p></div></div><p class="product-description">After my son was born, I quickly realized how little time we have on this earth and how quickly it passes. I built Dotted Line to remind myself of that and to live each day with intention.</p><p class="product-description">Dotted Line shows your day, week, month, and year in dots, with event countdowns, daily intentions, and Home Screen widgets. The core app is free on iPhone and iPad; a one-time Premium purchase unlocks widgets, custom colors, and the Mac app.</p>{actions}</section><section class="product-screenshots" aria-labelledby="screenshots-heading"><h2 id="screenshots-heading">Screenshots</h2>{gallery}</section><p class="page-note">Questions about Dotted Line? <a href="mailto:{{email}}">Email me.</a></p>'''


def blog(posts):
    return f'''<section class="page-intro blog-intro"><h1>Blog</h1><p>Posts on software, data science, and life.</p><a class="plain-link feed-link" href="../feed.xml">Subscribe via RSS</a></section><section class="blog-posts post-list" aria-label="Blog posts">{post_list(posts, '../')}</section><p class="page-note">Have a thought to share? <a href="mailto:{{email}}">Email me.</a></p>'''


def about(person_name):
    return f'''<section class="page-intro about-heading"><h1>About me</h1></section><div class="about-layout"><img class="about-photo" src="../assets/img/8-0-2.jpg" width="340" height="340" alt="Portrait of {escape(person_name, quote=True)}" decoding="async"><article class="prose about-copy"><p>I’m {escape(person_name)}, a software engineer, data scientist, and independent app developer.</p><p>I’ve spent more than 10 years in software engineering and more than 5 years in data science. I also make my own apps and write about my work and experiences.</p><p>You can find <a href="../apps/">my apps</a> and <a href="../blog/">my posts</a> here. I also recently started being active on <a href="https://x.com/novica93">X</a> again.</p><h2>Get in touch</h2><p>For questions, feedback, or ideas, email me at <a href="mailto:{{email}}">{{email}}</a>.</p></article></div>'''


def article(post):
    notice = '<p class="draft-notice">Draft preview — this post is excluded from the normal build.</p>' if post["draft"] else ""
    return f'''<div class="article-wrap"><a class="back-link" href="../">Back to the blog</a>{notice}<header class="article-header"><p class="post-meta"><time datetime="{post['published'].isoformat()}">{pretty_date(post['published'])}</time><span>{post['minutes']} min read</span></p><h1>{escape(post['title'])}</h1><p class="article-description">{escape(post['description'])}</p></header><article class="prose post-body">{post['body']}</article><footer class="article-footer"><a class="plain-link" href="mailto:{{email}}">Email me about this post</a><a class="back-link" href="../">Back to the blog</a></footer></div>'''


def migration_aliases(posts):
    """Only retain aliases for published posts that still exist."""
    if not MIGRATION.is_file():
        return {}
    migration = json.loads(MIGRATION.read_text(encoding="utf-8"))
    published = {f"/blog/{post['slug']}/" for post in posts if not post["draft"]}
    aliases = dict(migration.get("archive_aliases", {}))
    for record in migration["posts"]:
        if record["canonical_path"] in published:
            for path in record["legacy_paths"]:
                aliases[path] = record["canonical_path"]
    return aliases


def write_redirects(staging, aliases, site_url, draft_preview=False):
    for old, new in aliases.items():
        if not old.startswith("/") or not new.startswith("/") or old.startswith("//") or new.startswith("//"):
            raise ValueError("Legacy redirects must use local site paths")
        relative = unquote(old).lstrip("/")
        if any(part in ("..", ".") for part in Path(relative).parts):
            raise ValueError("Unsafe legacy path")
        target = staging / relative
        if old.endswith("/"):
            target /= "index.html"
        if target.exists():
            raise ValueError(f"Legacy path collides with a generated page: {old}")
        canonical = escape(site_url + new, quote=True)
        destination = escape(new, quote=True)
        robots = "noindex,nofollow" if draft_preview else "noindex,follow"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="{robots}"><title>Page moved</title><link rel="icon" href="data:,"><link rel="canonical" href="{canonical}"><meta http-equiv="refresh" content="0; url={destination}"></head><body><h1>This page has moved.</h1><p><a href="{destination}">Continue to the page</a>.</p></body></html>''', encoding="utf-8")


def write_feed(staging, posts, config):
    migration = json.loads(MIGRATION.read_text(encoding="utf-8")) if MIGRATION.is_file() else {"posts": []}
    original_guids = {post["canonical_path"]: post.get("feed_guid") for post in migration["posts"]}
    ET.register_namespace("atom", "http://www.w3.org/2005/Atom")
    root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(root, "channel")
    ET.SubElement(channel, "title").text = config["site_name"]
    ET.SubElement(channel, "link").text = config["url"] + "/"
    ET.SubElement(channel, "description").text = f"Apps, notes, and things {config['person_name']} is learning."
    ET.SubElement(channel, "{http://www.w3.org/2005/Atom}link", href=config["url"] + "/feed.xml", rel="self", type="application/rss+xml")
    for post in posts:
        if post["draft"]:
            continue
        item = ET.SubElement(channel, "item")
        url = config["url"] + f"/blog/{post['slug']}/"
        ET.SubElement(item, "title").text = post["title"]
        ET.SubElement(item, "link").text = url
        ET.SubElement(item, "guid", isPermaLink="true").text = original_guids.get(f"/blog/{post['slug']}/") or url
        timestamp = datetime.combine(post["published"], datetime.min.time(), tzinfo=timezone.utc)
        ET.SubElement(item, "pubDate").text = format_datetime(timestamp, usegmt=True)
        body = re.sub(r'(href|src)="([^"]+)"', lambda match:
                      f'{match[1]}="{escape(urljoin(url, unescape(match[2])), quote=True)}"', post["body"])
        ET.SubElement(item, "description").text = body
    ET.ElementTree(root).write(staging / "feed.xml", encoding="utf-8", xml_declaration=True)


def build(destination, include_drafts=False):
    destination = destination.resolve()
    if destination == ROOT or destination in ROOT.parents:
        raise ValueError("Choose a dedicated output directory")
    if destination.exists() and destination != ROOT / "dist" and not (destination / ".nova-generated").is_file():
        raise ValueError("Refusing to replace an existing directory that was not generated by this builder")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    person_name = config["person_name"]
    site_name = config["site_name"]
    site_url = config["url"].rstrip("/")
    parsed_url = urlsplit(site_url)
    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc or parsed_url.path or parsed_url.query or parsed_url.fragment:
        raise ValueError("site.json url must be an HTTP(S) origin without a path")
    config["url"] = site_url
    dotted_url = configured_app_url(config, "website_url")
    dotted_store_url = configured_app_url(config, "app_store_url")
    posts = read_posts(include_drafts)
    template = Template((SOURCE / "templates" / "base.html").read_text(encoding="utf-8"))
    styles_version = hashlib.sha256((SOURCE / "styles.css").read_bytes()).hexdigest()[:12]
    staging = destination.with_name(destination.name + ".building")
    if staging.exists():
        if not (staging / ".nova-generated").is_file():
            raise ValueError("Build staging directory is occupied; choose a different output directory")
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    (staging / ".nova-generated").write_text("Generated by the static site builder.\n", encoding="utf-8")
    shutil.copytree(SOURCE / "assets", staging / "assets")
    shutil.copy2(SOURCE / "styles.css", staging / "styles.css")
    # Attach local images to Markdown posts with ../../assets/blog/<filename>.
    images = ROOT / "content" / "images"
    if images.is_dir():
        shutil.copytree(images, staging / "assets" / "blog")
    canonical_paths = []

    def page(path, title, description, content, active, og_type="website"):
        depth = len(Path(path).parts) - 1
        root = "../" * depth if depth else "./"
        nav = []
        for label, route in (("Home", ""), ("Apps", "apps/"), ("Blog", "blog/"), ("About", "about/")):
            current = ' aria-current="page"' if label.lower() == active else ""
            nav.append(f'<a href="{root}{route}"{current}>{label}</a>')
        email = escape(config["email"], quote=True)
        content = content.replace("{email}", email)
        canonical_path = "/" + path.removesuffix("index.html")
        page_url = escape(site_url + canonical_path, quote=True)
        html = template.substitute(title=escape(title), description=escape(description, quote=True),
                                   content=content, root=root, navigation="".join(nav), email=email, styles_version=styles_version,
                                   year=date.today().year, og_type=og_type, person_name=escape(person_name), site_name=escape(site_name, quote=True), page_url=page_url,
                                   robots='<meta name="robots" content="noindex,nofollow">' if include_drafts else "")
        target = staging / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        if path != "404.html":
            canonical_paths.append(canonical_path)

    page("index.html", f"{site_name} — Apps, writing, and things I’m learning.",
         f"Hi, I’m {person_name}. Software engineer, data scientist, and independent app developer, with 10+ years in engineering and 5+ years in data science.", home(posts, person_name), "home")
    page("apps/index.html", f"Apps — {site_name}", f"Explore Dotted Line and the apps I make. Independently built by {person_name}.", apps(), "apps")
    page("apps/dotted/index.html", "Dotted Line — Time Progress & Countdown Widgets", "Track your day, week, month, and year in dots with Dotted Line. Event countdowns, daily intentions, and Home Screen widgets for iPhone, iPad, and Mac.", dotted(dotted_url, dotted_store_url), "apps")
    page("blog/index.html", f"Blog — {site_name}", f"Notes from {person_name} on software engineering, data science, and building things.", blog(posts), "blog")
    page("about/index.html", f"About — {site_name}", f"Hi, I’m {person_name}. Software engineer, data scientist, and independent app developer. My work and what I’m exploring.", about(person_name), "about")
    for post in posts:
        page(f"blog/{post['slug']}/index.html", f"{post['title']} — {site_name}", post["description"], article(post), "blog", "article")
    page("404.html", f"Page not found — {site_name}", "This page could not be found.",
         '<section class="page-intro"><h1>Page not found.</h1><p>The address may be incorrect, or the page may have moved.</p><a class="button" href="/">Go to home</a></section>', "")
    # A 404 can be served at any URL depth by the host.
    error = staging / "404.html"
    error.write_text(error.read_text(encoding="utf-8").replace('href="./', 'href="/'), encoding="utf-8")
    aliases = migration_aliases(posts)
    write_redirects(staging, aliases, site_url, include_drafts)
    write_feed(staging, posts, config)
    sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    # Draft preview URLs must never be advertised for indexing.
    for path in canonical_paths if not include_drafts else []:
        entry = ET.SubElement(sitemap, "url")
        ET.SubElement(entry, "loc").text = site_url + path
    ET.ElementTree(sitemap).write(staging / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    robots = "User-agent: *\nDisallow: /\n" if include_drafts else f"User-agent: *\nAllow: /\n\nSitemap: {site_url}/sitemap.xml\n"
    (staging / "robots.txt").write_text(robots, encoding="utf-8")
    (staging / "CNAME").write_text(parsed_url.hostname + "\n", encoding="utf-8")
    (staging / ".nojekyll").touch()
    if destination.exists():
        shutil.rmtree(destination)
    staging.rename(destination)
    print(f"Built {6 + len(posts)} pages and {len(aliases)} legacy redirects in {destination}; {len(posts)} post(s){' (draft preview)' if include_drafts else ''}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drafts", action="store_true", help="Include draft and future posts; noindex all preview pages")
    parser.add_argument("--output", type=Path, default=ROOT / "dist", help="Output directory; defaults to site/dist")
    args = parser.parse_args()
    try:
        build(args.output.resolve(), args.drafts)
    except (ValueError, KeyError) as error:
        sys.exit(f"Build failed: {error}")
