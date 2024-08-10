from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import generics
from main.models import *
from main.serializers import *
from main.tasks import *


@api_view(["GET"])
def download_cat(request):
    all_cats = Cat.objects.all()
    serializer = CatSerializer(all_cats, many=True)
    result = download_a_cat.delay()
    print(result)
    if request.method == "GET":
        return Response(serializer.data)
    return Response("Hello World")


class CatCreateAPIView(generics.CreateAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

