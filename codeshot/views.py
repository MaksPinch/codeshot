from django.shortcuts import render

from .forms import CodeInputForm
from .services.highlighting import highlight_code


def home_view(request):
    highlighted_code = None

    if request.method == "POST":
        form = CodeInputForm(request.POST)
        if form.is_valid():
            request.session["code"] = form.cleaned_data["code"]
            request.session["language"] = form.cleaned_data["language"]
            request.session["filename"] = form.cleaned_data["filename"]
            highlighted_code = highlight_code(
                form.cleaned_data["code"], form.cleaned_data["language"]
            )
    else:
        form = CodeInputForm(initial=get_initial_form_data(request))

    context = {
        "title": "CodeShot",
        "subtitle": "Create syntax-highlighted code previews.",
        "form": form,
        "highlighted_code": highlighted_code,
    }

    return render(request, "codeshot/home.html", context)


def get_initial_form_data(request):
    return {
        "code": request.session.get("code", 'print("Hello,CodeShot!")'),
        "language": request.session.get("language", "python"),
        "filename": request.session.get("filename", "main.py"),
    }
