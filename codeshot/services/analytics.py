from codeshot.models import ProductEvent

def record_product_event(event_name, editor_state=None, export_format=""):
    if editor_state is None:
        editor_state = {}

    return ProductEvent.objects.create(
        event_name=event_name,
        language=editor_state.get("language", ""),
        theme=editor_state.get("theme", ""),
        export_format=export_format
    )

