import pytest

from codeshot.services.exports import generate_image, ExportError

RANDDOME_SETTINGS = {
    "code": "print('export')",
    "language": "python",
    "filename": "export.py",
    "theme": "default",
    "font_size": 14,
    "padding": 24,
}


def test_generate_export_return_png_bytes():
    result = generate_image(RANDDOME_SETTINGS, "png")

    assert isinstance(result, bytes)
    assert result.startswith(b"\x89PNG")


def test_generate_export_return_jpg_bytes():
    result = generate_image(RANDDOME_SETTINGS, "jpg")

    assert isinstance(result, bytes)
    assert result.startswith(b"\xff\xd8")


def test_generate_export_return_unknownformat():
    with pytest.raises(ExportError):
        result = generate_image(RANDDOME_SETTINGS, "txt")
