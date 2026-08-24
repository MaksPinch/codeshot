from django.http import JsonResponse


def json_login_required(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        return view(request, *args, **kwargs)

    return wrapper


def json_permission_required(permission):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if not request.user.has_perm(permission):
                return JsonResponse({"error": "Permission denied"}, status=403)
            return view(request, *args, **kwargs)

        return wrapper

    return decorator
