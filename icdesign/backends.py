from django.contrib.auth.backends import BaseBackend
from pages.models import User


class CustomBackend(object):

    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            user = User.objects.get(ic_id=username, ic_pass=password)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

