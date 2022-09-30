from rest_framework import serializers
from .models import Image, Processing
from django.conf import settings


class ImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image
        fields = ['title', 'image', "type"]


class ProcessingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Processing
        fields = ['type1', 'type2', 'type3', "thresh", "kernel", "c", "k"]
