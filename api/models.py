from unicodedata import category
from django.db import models

# Create your models here.


def upload_path(instance, filename):
    return '/'.join(['images', "base", f"{instance.title}.png"])


class Processing(models.Model):
    type1 = models.CharField(max_length=32, default="none")
    type2 = models.CharField(max_length=32, default="none")
    type3 = models.CharField(max_length=32, default="none")
    thresh = models.CharField(max_length=32, default="127")
    kernel = models.CharField(max_length=32, default="15")
    c = models.CharField(max_length=32, default="5")
    k = models.CharField(max_length=32, default="0.2")


class Image(models.Model):
    title = models.CharField(max_length=32, blank=False)
    image = models.ImageField(blank=True, null=True, upload_to=upload_path)
    type = models.CharField(max_length=32, default="0")
