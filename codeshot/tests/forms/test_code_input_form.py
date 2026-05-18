from codeshot.froms import CodeInputForm


def test_code_input_form_accepts_valid_data():
    form = CodeInputForm(
        data={
            "code": "print('hello')",
            "language": "python",
            "filename": "hello.py",
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
