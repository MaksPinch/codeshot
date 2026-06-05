from .highlighting import highlight_code


def build_preview_context(cleaned_data):
    return {
        "highlighted_code": highlight_code(
            cleaned_data["code"],
            cleaned_data["language"],
        ),
        "preview_filename": cleaned_data.get("filename") or "main.py",
        "preview_theme": cleaned_data["theme"],
        "preview_font_size": cleaned_data["font_size"],
        "preview_padding": cleaned_data["padding"],
    }
