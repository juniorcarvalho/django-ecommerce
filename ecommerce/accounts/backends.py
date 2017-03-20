from django.contrib.auth.backends import ModelBackend as BaseModelBackend
from django.contrib.auth import get_user_model


class ModelBackend(BaseModelBackend):

    def authenticate(self, username=None, password=None):
        if not username is None:
            try:
                user = get_user_model().objects.get(email=username)
                if user.check_password(password):
                    return user
            except get_user_model().DoesNotExist:
                return None


