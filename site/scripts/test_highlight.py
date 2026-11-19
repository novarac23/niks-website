"""Verify syntax colors never change or execute a post's code examples."""

from html.parser import HTMLParser
import unittest

from highlight import code_block, python_html
from markdown import render


class Text(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.text = ""
        self.feed(source)

    def handle_data(self, data):
        self.text += data


class HighlightTests(unittest.TestCase):
    def test_python_tokens_and_whitespace_are_preserved(self):
        code = '\nimport re\n\n# Keep the spaces and tabs.\ndef example(value=42):\n\treturn print("hello", value is None)\n\n'
        html = python_html(code)
        self.assertEqual(Text(html).text, code)
        for token_type in ("keyword", "comment", "function", "number", "builtin", "string", "literal", "operator"):
            self.assertIn(f'class="syntax-{token_type}"', html)

    def test_multiline_strings_unicode_and_trailing_spaces(self):
        code = 'café = """First line\nSecond line: <tag> & 🥐\n"""  \n'
        html = python_html(code)
        self.assertEqual(Text(html).text, code)
        self.assertIn('class="syntax-string"', html)
        self.assertNotIn("<tag>", html)

    def test_keywords_inside_strings_and_comments_are_not_retokenized(self):
        html = python_html('message = "import # 42"\n# print(3)\nnumber = 42')
        self.assertEqual(html.count('class="syntax-keyword"'), 0)
        self.assertEqual(html.count('class="syntax-string"'), 1)
        self.assertEqual(html.count('class="syntax-comment"'), 1)
        self.assertEqual(html.count('class="syntax-number"'), 1)

    def test_incomplete_python_falls_back_without_losing_text(self):
        for source in ('value = """unfinished', "value = 'unfinished", 'print(42'):
            html = python_html(source)
            self.assertEqual(Text(html).text, source)
            self.assertNotIn('class="syntax-', html)

    def test_plain_output_is_labeled_and_not_highlighted(self):
        source = "import\n42\nTrue\n<tag>"
        html = code_block(source, "text")
        self.assertIn('class="code-block-header">Output<', html)
        self.assertNotIn('class="syntax-', html)
        self.assertIn("&lt;tag&gt;", html)
        self.assertIn('tabindex="0" role="region"', html)

    def test_code_cannot_inject_executable_markup(self):
        source = 'value = "</code><script>alert(1)</script>"'
        for language in ("python", "html", ""):
            html = code_block(source, language)
            self.assertNotIn("<script>", html)
            self.assertIn("&lt;script&gt;", html)

    def test_fenced_markdown_gets_accessible_static_highlighting(self):
        html = render("```python\nimport re\n```\n\n`inline_code`")
        self.assertIn('<figure class="code-block">', html)
        self.assertIn('aria-label="Python code"', html)
        self.assertIn('class="syntax-keyword">import</span>', html)
        self.assertIn("<code>inline_code</code>", html)


if __name__ == "__main__":
    unittest.main()
