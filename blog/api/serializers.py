#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/1 18:18
# @Author  : Dengsc
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm


from rest_framework import serializers
from app.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('name', 'image')
