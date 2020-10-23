from api import views
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path("login/", views.Login.as_view()),
    path("rp/", views.RegisterProduct.as_view()),
    path("follow/", views.Follow.as_view()),
    path("unfollow/", views.Unfollow.as_view()),
]
