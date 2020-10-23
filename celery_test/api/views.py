import json

from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .task import send_notification
from django_redis import get_redis_connection
from django.contrib.auth.models import User
from celery_test.authentication import CustomAuthentication


class Login(APIView):
    def get(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"message": "this method not allowed"})

    def post(self, request):
        pass


class RegisterProduct(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        data = request.data
        product, created = Product.objects.get_or_create(product_code=data.get("product_code"))
        Product.objects.update(product_count=F('product_count') + data.get("product_count"),
                               product_name=data.get("product_name"))
        if not created:
            send_notification.delay(product.product_code, product.product_name)
        return Response(status=status.HTTP_200_OK)


class Follow(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        data = request.data
        user = User.objects.get(username=data.get("username"))
        con = get_redis_connection("default")
        try:
            con.hmset(data.get("product_code"),
                      {user.username: json.dumps((user.email, user.first_name, user.last_name))})
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Unfollow(APIView):
    authentication_classes = (CustomAuthentication,)
    permission_classes = ()

    def post(self, request):
        if request.user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"text": "Authentication is needed"})

        data = request.data
        user = User.objects.get(username=data.get("username"))
        con = get_redis_connection("default")
        try:
            con.hdel(data.get("product_code"), user.username)
            return Response(status=status.HTTP_200_OK, data={"text": "done"})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
