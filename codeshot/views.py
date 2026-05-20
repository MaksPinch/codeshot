from django.shortcuts import render

from codeshot.forms import CodeInputForm


def home_view(request):
    if request.method == "POST":
        form = CodeInputForm(request.POST)
        if form.is_valid():
            preview_data = form.cleaned_data
        else:
            preview_data = None
    else:
        form = CodeInputForm()
        preview_data = None

    context = {
        "title": "CodeShot",
        "subtitle": "Create syntax-highlighted code previews.",
        "form": form,
        "preview_data": preview_data,
    }

    return render(request, "codeshot/home.html", context)
