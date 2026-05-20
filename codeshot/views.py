from django.shortcuts import render

from .froms import CodeInputForm
from .services.highlighting import highlight_code


def home_view(request):
    highlighted_code = None

    if request.method == "POST":
        form = CodeInputForm(request.POST)
        if form.is_valid():
            highlighted_code = highlight_code(
                form.cleaned_data["code"], form.cleaned_data["language"]
            )
    else:
        form = CodeInputForm()

    context = {
        "title": "CodeShot",
        "subtitle": "Create syntax-highlighted code previews.",
        "form": form,
        "highlighted_code": highlighted_code,
    }

    return render(request, "codeshot/home.html", context)

