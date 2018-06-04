# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from serializers import ImageSerializer
from app.models import Image


class ImageViewSet(viewsets.ModelViewSet):
    """
    upload image
    """

    def create(self, request, *args, **kwargs):
        data = {
            'success': 0,  # 0表示上传失败，1表示上传成功
            'message': '',
            'url': ''
        }
        file = request.data.dict()
        print file
        self.serializer_class = ImageSerializer
        serial = ImageSerializer(data=file)
        if not serial.is_valid():
            data['message'] = 'serial is not valid!'
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj = serial.save()
        data['success'] = 1
        data['url'] = obj.image.url
        return Response(data)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ImageSerializer
        self.queryset = Image.objects.all()
        return super(ImageViewSet, self).list(request)
