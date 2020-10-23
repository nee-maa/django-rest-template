from django.contrib.auth.models import User
from rest_framework import status
from django.http import HttpResponseBadRequest, HttpResponse


class CustomAuthentication:
    def authenticate(self, request, token=None):
        username = request.data.get("username")
        if not username:
            return None, None

        try:
            user = User.objects.get(username=username)
            request.user = user
            return request, token
        except User.DoesNotExist:
            return None, None
