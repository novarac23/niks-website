"""Build-time Python syntax highlighting using the standard library lexer.

Token positions preserve the original code exactly. Other languages and
incomplete Python examples fall back to escaped, unhighlighted text.
"""

import builtins
import html
import io
import keyword
import token
import tokenize

BUILTINS = frozenset(dir(builtins))
IGNORED = {token.ENCODING, token.ENDMARKER, token.NEWLINE, token.NL, token.INDENT, token.DEDENT}
LABELS = {"python": "Python", "py": "Python", "python3": "Python", "text": "Output",
          "plaintext": "Plain text", "output": "Output", "console": "Console"}


def python_html(source):
    try:
        tokens = [item for item in tokenize.generate_tokens(io.StringIO(source).readline)
                  if item.type not in IGNORED]
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return html.escape(source)
    if any(item.type == token.ERRORTOKEN and not item.string.isspace() for item in tokens):
        return html.escape(source)

    offsets = [0]
    for line in source.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))

    def position(point):
        row, column = point
        return offsets[min(row - 1, len(offsets) - 1)] + column

    result = []
    cursor = 0
    for index, item in enumerate(tokens):
        start, end = position(item.start), position(item.end)
        kind = None
        previous = tokens[index - 1].string if index else ""
        following = tokens[index + 1].string if index + 1 < len(tokens) else ""
        if item.type == token.COMMENT:
            kind = "comment"
        elif item.type == token.STRING:
            kind = "string"
        elif item.type == token.NUMBER:
            kind = "number"
        elif item.type == token.OP:
            kind = "operator"
        elif item.type == token.NAME:
            if item.string in ("True", "False", "None"):
                kind = "literal"
            elif keyword.iskeyword(item.string):
                kind = "keyword"
            elif previous in ("def", "class"):
                kind = "function"
            elif previous != "." and item.string in BUILTINS:
                kind = "builtin"
            elif following == "(":
                kind = "function"
        result.append(html.escape(source[cursor:start]))
        value = html.escape(source[start:end])
        result.append(f'<span class="syntax-{kind}">{value}</span>' if kind else value)
        cursor = end
    result.append(html.escape(source[cursor:]))
    return "".join(result)


def code_block(source, language=""):
    language = language.lower()
    label = LABELS.get(language, language.upper() if language else "Plain text")
    body = python_html(source) if language in ("python", "py", "python3") else html.escape(source)
    css = f' class="language-{html.escape(language, quote=True)}"' if language else ""
    label = html.escape(label)
    return (f'<figure class="code-block"><figcaption class="code-block-header">{label}</figcaption>'
            f'<pre tabindex="0" role="region" aria-label="{label} code"><code{css}>{body}</code></pre></figure>')
