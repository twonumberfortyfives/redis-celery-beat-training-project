from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from main import views

app_name = "main"


urlpatterns = [
    path("download-cat/", views.download_cat, name="download_cat"),
    path("create-cat/", views.CatCreateAPIView.as_view(), name="create_cat"),
]

