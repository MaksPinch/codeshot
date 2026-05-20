from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer, get_lexer_by_name


def highlight_code(code, language):
    try:
        lexer = get_lexer_by_name(language)
    except Exception:
        lexer = PythonLexer()

    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)
