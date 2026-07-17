import io
from PIL import Image

class ExportError(Exception):
    pass

def generate_image(settings, format):
    frmt = format.lower()

    if frmt == "png":
        mode = "RGBA"
        save_format = "PNG"
    elif frmt in ("jpg", "jpeg"):
        mode = "RGB"
        save_format = "JPEG"
    else:
        raise ExportError(f"Unsupported image format: {format}")
    image = Image.new(mode, (100,100), "white")

    buffer = io.BytesIO()
    image.save(buffer, save_format)

    return buffer.getvalue()
