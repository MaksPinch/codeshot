from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.util import ClassNotFound

def highlight_code(code, language):
    try:
        lexer = get_lexer_by_name(language)
    except ClassNotFound:
        lexer = PythonLexer()

    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)
    