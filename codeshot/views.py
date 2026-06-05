from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import CodeInputForm
from .services.preview import build_preview_context


def persist_form_data(request, cleaned_data):
    for field_name in ["code", "language", "filename", "theme", "font_size", "padding"]:
        request.session[field_name] = cleaned_data[field_name]


def home_view(request):
    preview_context = {}

    if request.method == "POST":
        form = CodeInputForm(request.POST)
        if form.is_valid():
            preview_context = build_preview_context(form.cleaned_data)
            persist_form_data(request, form.cleaned_data)
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


@csrf_exempt
@require_POST
def preview_view(request):
    form = CodeInputForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)
    preview_context = build_preview_context(form.cleaned_data)
    return JsonResponse(
        {
            "highlighted_code": preview_context["highlighted_code"],
            "filename": preview_context["preview_filename"],
            "theme": preview_context["preview_theme"],
            "font_size": preview_context["preview_font_size"],
            "padding": preview_context["preview_padding"],
        }
    )
