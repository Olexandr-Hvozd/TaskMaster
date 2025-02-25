from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model.objects.filter(email=username).first()
            if user and user.check_password(password):
                return user
            return None
        except user_model.DoesNotExist:
            return None
