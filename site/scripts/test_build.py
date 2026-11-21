"""Integration checks for publication and a portable static export."""

from contextlib import redirect_stdout
from datetime import date, timedelta
from html.parser import HTMLParser
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit
import json
import xml.etree.ElementTree as ET

import build
from markdown import render


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = []
        self.links = []
        self.h1_count = 0
        self.current = []
        self.redirect = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])
        if tag == "h1":
            self.h1_count += 1
        if attrs.get("aria-current") == "page":
            self.current.append(attrs.get("href"))
        if tag == "meta" and attrs.get("http-equiv") == "refresh":
            self.redirect = attrs["content"].split("url=", 1)[1]


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.posts = self.base / "posts"
        self.posts.mkdir()
        self.output = self.base / "output"
        self.patch = patch.object(build, "POSTS", self.posts)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def post(self, slug, title="A post", draft="false", when=None, body="## Notes\n\nSome **useful** ideas."):
        when = when or date.today().isoformat()
        path = self.posts / f"{slug}.md"
        path.write_text(f"---\ntitle: {title}\ndate: {when}\ndescription: A short description.\ndraft: {draft}\n---\n\n{body}\n", encoding="utf-8")
        return path

    def build(self, drafts=False):
        with redirect_stdout(io.StringIO()):
            build.build(self.output, drafts)

    def test_published_posts_sort_and_drafts_have_no_public_route(self):
        self.post("older", "Older post", when="2020-01-01")
        self.post("newer", "Newer post", when="2021-01-01")
        self.post("private", "Private draft", draft="true")
        self.post("future", "Future post", when=(date.today() + timedelta(days=1)).isoformat())
        self.build()
        for filename in ("index.html", "blog/index.html"):
            source = (self.output / filename).read_text()
            self.assertLess(source.index("Newer post"), source.index("Older post"))
            self.assertNotIn("Private draft", source)
            self.assertNotIn("Future post", source)
        self.assertTrue((self.output / "blog/newer/index.html").is_file())
        self.assertFalse((self.output / "blog/private").exists())
        self.assertFalse((self.output / "blog/future").exists())

    def test_draft_preview_is_labeled_and_noindex(self):
        self.post("private", "Private draft", draft="true")
        self.build(drafts=True)
        self.assertIn("Draft preview", (self.output / "blog/index.html").read_text())
        self.assertIn("Draft preview", (self.output / "blog/private/index.html").read_text())
        for path in self.output.rglob("*.html"):
            self.assertIn('content="noindex,nofollow"', path.read_text())

    def test_unpublishing_removes_stale_page(self):
        self.post("a-post")
        self.build()
        self.assertTrue((self.output / "blog/a-post/index.html").is_file())
        self.post("a-post", draft="true")
        self.build()
        self.assertFalse((self.output / "blog/a-post").exists())
        self.assertIn("No posts yet.", (self.output / "blog/index.html").read_text())

    def test_failed_post_keeps_previous_output(self):
        self.post("a-post")
        self.build()
        previous = (self.output / "index.html").read_bytes()
        self.post("bad-post", when="not-a-date")
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(previous, (self.output / "index.html").read_bytes())
        self.assertTrue((self.output / "blog/a-post/index.html").exists())

    def test_article_metadata_and_markdown_are_escaped(self):
        self.post("escaping", title='Things <script> & "quotes"', body='## Heading\n\n<script>alert(1)</script>\n\n```html\n<b>code</b>\n```')
        self.build()
        source = (self.output / "blog/escaping/index.html").read_text()
        article_source = source.split('<main id="main"', 1)[1].split('</main>', 1)[0]
        self.assertNotIn("<script", article_source.lower())
        self.assertIn("&lt;script&gt;", source)
        self.assertIn("&lt;b&gt;code&lt;/b&gt;", source)
        self.assertEqual(Page(source).h1_count, 1)

    def test_static_routes_assets_and_navigation_resolve(self):
        self.post("sample-post", body="## Example\n\n[All apps](../../apps/) and **some writing**.\n\n::: dotted-screenshots")
        self.build()
        for path in self.output.rglob("*.html"):
            page = Page(path.read_text())
            self.assertEqual(page.h1_count, 1, path)
            self.assertEqual(len(page.ids), len(set(page.ids)), path)
            expected_current = 0 if path.name == "404.html" or page.redirect else 1
            self.assertEqual(len(set(page.current)), expected_current, path)
            self.assertEqual(len(page.current), expected_current * 2, path)
            for link in page.links:
                url = urlsplit(link)
                if url.scheme or url.netloc:
                    continue
                target = ((self.output / url.path.lstrip("/")) if url.path.startswith("/") else path.parent / unquote(url.path)).resolve()
                if target.is_dir():
                    target /= "index.html"
                if not url.path:
                    target = path
                self.assertTrue(target.is_file(), f"{path}: broken link {link}")
                if url.fragment:
                    self.assertIn(url.fragment, Page(target.read_text()).ids, f"{path}: missing fragment {link}")

    def test_output_guard_preserves_unrelated_directory(self):
        self.output.mkdir()
        sentinel = self.output / "keep.txt"
        sentinel.write_text("Keep this")
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(sentinel.read_text(), "Keep this")

    def test_missing_draft_defaults_to_unpublished(self):
        path = self.post("unfinished")
        path.write_text(path.read_text().replace("draft: false\n", ""))
        self.build()
        self.assertFalse((self.output / "blog/unfinished").exists())

    def test_legacy_routes_canonical_and_removal_on_unpublish(self):
        self.post("migrated", when="2020-01-02")
        manifest = self.base / "migration.json"
        manifest.write_text(json.dumps({"posts": [{"canonical_path": "/blog/migrated/", "feed_guid": "http://novarac.com/life/2020/01/02/migrated.html", "legacy_paths": ["/migrated/", "/life/2020/01/02/migrated.html"]}]}))
        with patch.object(build, "MIGRATION", manifest):
            self.build()
            for name in ("migrated/index.html", "life/2020/01/02/migrated.html"):
                source = (self.output / name).read_text()
                self.assertEqual(Page(source).redirect, "/blog/migrated/")
                self.assertIn('href="https://novarac.com/blog/migrated/"', source)
            self.assertEqual(ET.parse(self.output / "feed.xml").findtext("channel/item/guid"), "http://novarac.com/life/2020/01/02/migrated.html")
            self.post("migrated", draft="true")
            self.build()
            self.assertFalse((self.output / "migrated").exists())
            self.assertFalse((self.output / "life").exists())

    def test_feed_and_sitemap_exclude_drafts_and_use_real_domain(self):
        self.post("live", body="## Example\n\n[Apps](../../apps/) and ![Image](../../assets/img/example.png)")
        self.post("private", draft="true")
        self.build(drafts=True)
        feed = ET.parse(self.output / "feed.xml")
        items = feed.findall("channel/item")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].findtext("link"), "https://novarac.com/blog/live/")
        self.assertIn('src="https://novarac.com/assets/img/example.png"', items[0].findtext("description"))
        self.assertIn('href="https://novarac.com/apps/"', items[0].findtext("description"))
        self.assertEqual(list(ET.parse(self.output / "sitemap.xml").getroot()), [])
        self.build()
        sitemap = (self.output / "sitemap.xml").read_text()
        self.assertIn("https://novarac.com/blog/live/", sitemap)
        self.assertNotIn("/private/", sitemap)
        self.assertNotIn("404.html", sitemap)

    def test_app_overview_links_to_marketing_site_and_catalog_stays_local(self):
        config = json.loads(build.CONFIG.read_text())
        config["apps"] = {"dotted": {"website_url": "https://dotted.novarac.com/?from=site&view=home"}}
        config_path = self.base / "site.json"
        config_path.write_text(json.dumps(config))
        with patch.object(build, "CONFIG", config_path):
            self.build()
        for name, root in (("index.html", "./"), ("apps/index.html", "../")):
            source = (self.output / name).read_text()
            self.assertIn(f'<a class="app-card" href="{root}apps/dotted/">', source)
            self.assertIn("<h3>Dotted</h3>", source)
        detail = (self.output / "apps/dotted/index.html").read_text()
        self.assertIn("Visit Dotted’s website", detail)
        self.assertIn('href="https://dotted.novarac.com/?from=site&amp;view=home"', detail)

    def test_invalid_app_url_preserves_previous_build(self):
        self.build()
        previous = (self.output / "index.html").read_bytes()
        config = json.loads(build.CONFIG.read_text())
        config["apps"] = {"dotted": {"website_url": "javascript:alert(1)"}}
        config_path = self.base / "site.json"
        config_path.write_text(json.dumps(config))
        with patch.object(build, "CONFIG", config_path):
            with self.assertRaisesRegex(ValueError, "website_url"):
                self.build()
        self.assertEqual((self.output / "index.html").read_bytes(), previous)

    def test_app_store_link_can_appear_beside_website_or_on_its_own(self):
        config = json.loads(build.CONFIG.read_text())
        config_path = self.base / "site.json"
        for website in ("https://dotted.novarac.com", None):
            config["apps"] = {"dotted": {"website_url": website, "app_store_url": "https://apps.apple.com/app/id6760857931"}}
            config_path.write_text(json.dumps(config))
            with patch.object(build, "CONFIG", config_path):
                self.build()
            source = (self.output / "apps/dotted/index.html").read_text()
            self.assertIn('href="https://apps.apple.com/app/id6760857931"', source)
            self.assertIn("View on the App Store", source)
            self.assertEqual("Visit Dotted’s website" in source, website is not None)

    def test_invalid_app_store_url_is_rejected(self):
        config = json.loads(build.CONFIG.read_text())
        config["apps"] = {"dotted": {"app_store_url": "javascript:alert(1)"}}
        config_path = self.base / "site.json"
        config_path.write_text(json.dumps(config))
        with patch.object(build, "CONFIG", config_path):
            with self.assertRaisesRegex(ValueError, "app_store_url"):
                self.build()


class MarkdownTests(unittest.TestCase):
    def test_dotted_gallery_is_shared_accessible_and_keeps_surrounding_prose(self):
        from gallery import dotted_screenshots

        gallery = dotted_screenshots()
        self.assertIn(gallery, build.dotted())
        result = render("Before\n::: dotted-screenshots\nAfter")
        self.assertEqual(result, "<p>Before</p>\n" + gallery + "\n<p>After</p>")
        self.assertEqual(gallery.count("<figure>"), 4)
        self.assertIn('role="region"', gallery)
        self.assertIn('tabindex="0"', gallery)
        self.assertEqual(gallery.count('width="1206" height="2622"'), 4)

    def test_gallery_directive_is_literal_in_code_and_inline_prose(self):
        self.assertNotIn('class="screenshot-gallery"', render("```text\n::: dotted-screenshots\n```"))
        self.assertEqual(render("Use ::: dotted-screenshots here."), "<p>Use ::: dotted-screenshots here.</p>")

    def test_supported_writing_formats(self):
        result = render("## Heading\n\nA **bold** and *italic* thought with `code`.\n\n- One\n- Two\n\n1. First\n2. Second\n\n> A quote\n\n---\n\n![An image](../../assets/blog/image.jpg)\n\n[A link](https://example.com/?a=1&b=2)")
        for expected in ('<h2 id="heading">', "<strong>bold</strong>", "<em>italic</em>", "<code>code</code>", "<ul>", "<ol>", "<blockquote>", "<hr>", 'alt="An image"', "a=1&amp;b=2"):
            self.assertIn(expected, result)

    def test_code_is_not_interpreted_as_markdown(self):
        self.assertIn("<code>**literal**</code>", render("`**literal**`"))

    def test_script_links_are_rejected(self):
        with self.assertRaises(ValueError):
            render("[Bad](javascript:alert)")
        with self.assertRaises(ValueError):
            render("![Bad](data:text/html,test)")

    def test_unclosed_code_fence_fails_clearly(self):
        with self.assertRaisesRegex(ValueError, "Unclosed code fence"):
            render("```python\nprint('unfinished')")

    def test_imported_punctuation_emphasis_bullets_and_anchors(self):
        text = '''Here\\'s a thought.\n\n## Have a \\"school\\" day\n\n_Thanks to [a reviewer](https://example.com)._\n\n• First idea\n\n• Another idea\n\n## Same heading\n\n## Same heading'''
        result = render(text)
        self.assertIn("Here's a thought.", result)
        self.assertIn('id="have-a-school-day"', result)
        self.assertIn('<em>Thanks to <a href="https://example.com">a reviewer</a>.</em>', result)
        self.assertIn("<li>First idea</li>", result)
        self.assertIn('id="same-heading"', result)
        self.assertIn('id="same-heading-1"', result)
        self.assertNotIn("\x00", result)


if __name__ == "__main__":
    unittest.main()
