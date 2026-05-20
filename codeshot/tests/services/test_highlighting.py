from codeshot.services.highlighting import highlight_code

def test_highlight_code_returns_html():
    result = highlight_code("print('Hello World!')", "python")
    assert "<div class=\"highlight\"" in result
    assert "print" in result

def test_highlight_code_falls_back_for_unknown_language():
    result = highlight_code("print('Hello World!')", "unknown-language")
    assert "<div class=\"highlight\"" in result


