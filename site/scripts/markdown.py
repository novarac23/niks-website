"""Small, dependency-free Markdown renderer for this site's text-first blog.

Supports headings, paragraphs, lists, quotes, rules, fenced code, images,
links, emphasis, and inline code. Raw HTML is escaped. This is an intentionally
bounded Markdown subset, not a CommonMark implementation.
"""

import html
import re
import string
from urllib.parse import urlsplit

from highlight import code_block


def safe_url(value, image=False):
    value = html.unescape(value).strip()
    scheme = urlsplit(value).scheme.lower()
    if scheme not in ("", "https", "http", "mailto") or (image and scheme == "mailto"):
        raise ValueError("Links must be relative, HTTPS, HTTP, or mailto URLs")
    if any(ord(char) < 32 for char in value):
        raise ValueError("Control characters are not allowed in URLs")
    return html.escape(value, quote=True)


def inline(text):
    if "\x00" in text:
        raise ValueError("Null characters are not supported in Markdown")
    tokens = []

    def keep(value):
        tokens.append(value)
        return f"\x00{len(tokens)-1}\x00"

    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", lambda m: keep(f"<code>{m[1]}</code>"), text)
    text = re.sub(r"\\([" + re.escape(string.punctuation) + r"])", lambda m: keep(m[1]), text)
    text = re.sub(r"!\[([^\]]*)\]\(([^\s)]+)\)", lambda m: keep(
        f'<img src="{safe_url(m[2], image=True)}" alt="{html.escape(html.unescape(m[1]), quote=True)}" loading="lazy">'), text)
    text = re.sub(r"\[([^\]]+)\]\(([^\s)]+)\)", lambda m: keep(
        f'<a href="{safe_url(m[2])}">{m[1]}</a>'), text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w])_([^_\n]+)_(?![\w])", r"<em>\1</em>", text)
    while re.search(r"\x00\d+\x00", text):
        text = re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m[1])], text)
    return text


def render(text):
    lines = text.replace("\r\n", "\n").splitlines()
    output = []
    index = 0
    heading_ids = {}

    def special(line):
        return re.match(r"\s*(?:#{1,6}\s|```|>|[-*+•]\s|\d+\.\s|---\s*$|\*\*\*\s*$)", line)

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        fence = re.match(r"^```([a-zA-Z0-9_-]*)\s*$", line)
        if fence:
            code = []
            index += 1
            while index < len(lines) and lines[index].strip() != "```":
                code.append(lines[index])
                index += 1
            if index == len(lines):
                raise ValueError("Unclosed code fence")
            output.append(code_block("\n".join(code), fence[1]))
            index += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            # The article title is already the page's H1.
            level = max(2, len(heading[1]))
            content = inline(heading[2])
            label = html.unescape(re.sub(r"<[^>]+>", "", content))
            slug = re.sub(r"[^\w\s-]", "", label.lower())
            slug = re.sub(r"[\s_]+", "-", slug).strip("-") or "section"
            count = heading_ids.get(slug, 0)
            heading_ids[slug] = count + 1
            identifier = f"{slug}-{count}" if count else slug
            output.append(f'<h{level} id="{identifier}">{content}</h{level}>')
            index += 1
            continue
        if re.fullmatch(r"\s*(---|\*\*\*)\s*", line):
            output.append("<hr>")
            index += 1
            continue
        if line.startswith(">"):
            quote = []
            while index < len(lines) and lines[index].startswith(">"):
                quote.append(re.sub(r"^> ?", "", lines[index]))
                index += 1
            output.append("<blockquote>" + render("\n".join(quote)) + "</blockquote>")
            continue
        item = re.match(r"^\s*([-*+•]|\d+\.)\s+(.+)$", line)
        if item:
            ordered = item[1][0].isdigit()
            kind = "ol" if ordered else "ul"
            items = []
            while index < len(lines):
                item = re.match(r"^\s*([-*+•]|\d+\.)\s+(.+)$", lines[index])
                if not item or item[1][0].isdigit() != ordered:
                    break
                items.append("<li>" + inline(item[2]) + "</li>")
                index += 1
            output.append(f"<{kind}>" + "".join(items) + f"</{kind}>")
            continue
        paragraph = [line.strip()]
        index += 1
        while index < len(lines) and lines[index].strip() and not special(lines[index]):
            paragraph.append(lines[index].strip())
            index += 1
        output.append("<p>" + inline(" ".join(paragraph)) + "</p>")
    return "\n".join(output)
