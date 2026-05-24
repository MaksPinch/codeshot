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

    THEME_CHOICES = [
        ("default", "Default"),
        ("dracula", "Dracula"),
        ("monokai", "Monokai"),
    ]
    theme = forms.ChoiceField(choices=THEME_CHOICES, initial="default")
    font_size = forms.IntegerField(min_value=10, max_value=32, initial=14)
    padding = forms.IntegerField(min_value=8, max_value=64, initial=24)
