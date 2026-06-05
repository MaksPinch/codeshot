from django.shortcuts import render

from .forms import CodeInputForm
from .services.preview import build_preview_context


def home_view(request):
    preview_context = {}

    if request.method == "POST":
        form = CodeInputForm(request.POST)
        if form.is_valid():
            preview_context = build_preview_context(form.cleaned_data)

            request.session["code"] = form.cleaned_data["code"]
            request.session["language"] = form.cleaned_data["language"]
            request.session["filename"] = form.cleaned_data["filename"]
            request.session["theme"] = form.cleaned_data["theme"]
            request.session["font_size"] = form.cleaned_data["font_size"]
            request.session["padding"] = form.cleaned_data["padding"]

    else:
        form = CodeInputForm(initial=get_initial_form_data(request))

    context = {
        "title": "CodeShot",
        "subtitle": "Create syntax-highlighted code previews.",
        "form": form,
        **preview_context,
    }

    return render(request, "codeshot/home.html", context)


def get_initial_form_data(request):
    return {
        "code": request.session.get("code", 'print("Hello,CodeShot!")'),
        "language": request.session.get("language", "python"),
        "filename": request.session.get("filename", "main.py"),
    }
