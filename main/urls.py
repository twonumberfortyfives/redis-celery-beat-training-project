from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path("download-cat/", views.download_cat, name="download_cat"),
]
