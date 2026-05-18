from django import forms


class CodeInputForm(forms.Form):
    LANGUAGE_CHOICES = [
        ("python", "Python"),
        ("javascript", "JavaScript"),
    ]
    code = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 12}),
        initial='print("Hello, CodeShot!")',
    )
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, initial="python")
    filename = forms.CharField(max_length=100, required=False, initial="main.py")
