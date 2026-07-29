import io
import logging

from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .decorators import json_login_required, json_permission_required
from .forms import CodeInputForm, LoginForm, RegisterForm
from .models import ProductEvent
from .services.analytics import get_product_event_summary, record_product_event
from .services.auth import create_user, serialize_user
from .services.exports import ExportError, generate_image
from .services.preview import build_preview_context
from .services.state import get_editor_state


def not_implemented_yet(request):
    return HttpResponse("Method is not implemented yet", status=501)


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
        "code": request.session.get("code", 'print("Hello, CodeShot!")'),
        "language": request.session.get("language", "python"),
        "filename": request.session.get("filename", "main.py"),
        "theme": request.session.get("theme", "monokai"),
        "font_size": request.session.get("font_size", 14),
        "padding": request.session.get("padding", 16),
    }


@require_POST
def preview_view(request):
    form = CodeInputForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)
    persist_form_data(request, form.cleaned_data)
    preview_context = build_preview_context(form.cleaned_data)
    record_product_event(ProductEvent.PREVIEW_CREATED, form.cleaned_data)
    return JsonResponse(
        {
            "highlighted_code": preview_context["highlighted_code"],
            "filename": preview_context["preview_filename"],
            "theme": preview_context["preview_theme"],
            "font_size": preview_context["preview_font_size"],
            "padding": preview_context["preview_padding"],
        }
    )


logger = logging.getLogger(__name__)


def helper_download_response(request, image_format, file_name):
    editor_state = get_editor_state(request.session)
    record_product_event(
        event_name=ProductEvent.EXPORT_STARTED,
        editor_state=editor_state,
        export_format=image_format,
    )
    try:
        image_bytes = generate_image(editor_state, image_format)
        buffer = io.BytesIO(image_bytes)
        record_product_event(
            event_name=ProductEvent.EXPORT_COMPLETED,
            editor_state=editor_state,
            export_format=image_format,
        )
        return FileResponse(buffer, as_attachment=True, filename=file_name)
    except ExportError:
        logger.exception("Failed to generate %s format", image_format)
        record_product_event(
            event_name=ProductEvent.EXPORT_FAILED,
            editor_state=editor_state,
            export_format=image_format,
        )
        return HttpResponse("Could not generate image export.", status=500)


def download_png_view(request):
    return helper_download_response(
        request, image_format="png", file_name="codeshot.png"
    )


def download_jpg_view(request):
    return helper_download_response(
        request, image_format="jpg", file_name="codeshot.jpg"
    )


def health_view(request):
    return JsonResponse({"status": "ok"})


@json_login_required
@json_permission_required("codeshot.view_product_stats")
def stats_view(request):
    return JsonResponse(get_product_event_summary())


@require_POST
def register_user(request):
    form = RegisterForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)
    user = create_user(form.cleaned_data)
    login(request, user)
    serialized_user = serialize_user(user)
    return JsonResponse(
        {"message": "User is registered", "user": serialized_user}, status=201
    )


@require_POST
def login_user(request):
    form = LoginForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)
    user = authenticate(
        request,
        username=form.cleaned_data["username"],
        password=form.cleaned_data["password"],
    )
    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=401)
    login(request, user)
    serialized_user = serialize_user(user)
    return JsonResponse({"user": serialized_user})


@require_POST
def logout_user(request):
    logout(request)
    return HttpResponse(status=204)


def me_information(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    serialized_user = serialize_user(request.user)
    return JsonResponse({"user": serialized_user})
