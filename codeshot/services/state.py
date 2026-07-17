def get_editor_state(session):
    settings = {
        "code": session.get("code", 'print("Hello, CodeShot!")'),
        "language": session.get("language", "python"),
        "filename": session.get("filename", "main.py"),
        "theme": session.get("theme", "default"),
        "font_size": session.get("font_size", 14),
        "padding": session.get("padding", 16),
    }

    return settings
