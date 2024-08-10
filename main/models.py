from django.db import models


class Cat(models.Model):
    url = models.CharField(max_length=1000)
