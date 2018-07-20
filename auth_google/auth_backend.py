from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class PasswordLessAuth(ModelBackend):
    def authenticate(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
