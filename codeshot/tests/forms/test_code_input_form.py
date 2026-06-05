from codeshot.forms import CodeInputForm


def test_code_input_form_accepts_valid_data():
    form = CodeInputForm(
        data={
            "code": "print('hello')",
            "language": "python",
            "filename": "hello.py",
            "theme": "default",
            "font_size": 14,
            "padding": 24
        }
    )
    assert form.is_valid()
    assert form.cleaned_data["code"] == "print('hello')"


def test_code_input_form_rejects_empty_code():
    form = CodeInputForm(
        data={
            "code": "",
            "language": "python",
            "filename": "hello.py",
        }
    )
    assert not form.is_valid()
    assert "code" in form.errors


def test_code_input_form_accepts_preview_settings():
    form = CodeInputForm(
        data={
            "code": "print('hello')",
            "language": "python",
            "filename": "hello.py",
            "theme": "dracula",
            "font_size": 16,
            "padding": 32,
        }
    )
    assert form.is_valid()
    assert form.cleaned_data["theme"] == "dracula"
