"""Verify a content-only import, including provenance and original assets."""

from contextlib import redirect_stdout
import hashlib
import io
from pathlib import Path
import tempfile
import unittest

from import_jekyll import import_posts


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "original"
        self.target = self.base / "new"
        (self.source / "_posts").mkdir(parents=True)
        (self.source / "assets/img").mkdir(parents=True)
        (self.source / "assets/img/chart.png").write_bytes(b"original image bytes")
        (self.source / "_config.yml").write_text('url: "http://novarac.com"\n')
        (self.source / "old-theme.css").write_text("do not import")
        self.post = self.source / "_posts/2020-01-02-example.md"
        self.post.write_text('''---
layout: post
title: Original Title
category: data science & engineering
description: Original description.
---

Here\\'s the original text.

![chart]({{ site.url }}/assets/img/chart.png)

```python
original_code = "unchanged"
```

[Earlier post](https://novarac.com/example/)
''')

    def run_import(self):
        with redirect_stdout(io.StringIO()):
            return import_posts(self.source, self.target)

    def test_content_metadata_images_and_source_preservation(self):
        before = {path.relative_to(self.source): path.read_bytes() for path in self.source.rglob("*") if path.is_file()}
        manifest = self.run_import()
        migrated = (self.target / "content/posts/example.md").read_text()
        self.assertIn("title: Original Title\ndate: 2020-01-02", migrated)
        self.assertIn("category: data science & engineering", migrated)
        self.assertIn("Here\\'s the original text.", migrated)
        self.assertIn('original_code = "unchanged"', migrated)
        self.assertIn("![chart](../../assets/img/chart.png)", migrated)
        self.assertIn("[Earlier post](../example/)", migrated)
        self.assertEqual((self.target / "src/assets/img/chart.png").read_bytes(), b"original image bytes")
        self.assertFalse((self.target / "old-theme.css").exists())
        self.assertEqual(before, {path.relative_to(self.source): path.read_bytes() for path in self.source.rglob("*") if path.is_file()})
        self.assertEqual(manifest["posts"][0]["source_sha256"], hashlib.sha256(before[Path("_posts/2020-01-02-example.md")]).hexdigest())
        self.assertEqual(manifest["posts"][0]["feed_guid"], "http://novarac.com/data%20science%20&%20engineering/2020/01/02/example.html")

    def test_repeat_is_safe_and_user_edits_are_preserved(self):
        self.run_import()
        self.run_import()
        target = self.target / "content/posts/example.md"
        target.write_text(target.read_text() + "\nA new edit.\n")
        with self.assertRaisesRegex(ValueError, "Existing content differs"):
            self.run_import()
        self.assertTrue(target.read_text().endswith("A new edit.\n"))


if __name__ == "__main__":
    unittest.main()
