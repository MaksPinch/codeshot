from django.contrib.auth import get_user_model


def auth_user(cleaned_data):
    User = get_user_model()
    return User.objects.create_user(
        username=cleaned_data["username"], password=cleaned_data["password"]
    )
