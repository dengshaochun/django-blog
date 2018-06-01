#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/1 18:56
# @Author  : Dengsc
# @Site    : 
# @File    : urls.py
# @Software: PyCharm


from django.conf.urls import url, include
from rest_framework import routers
from api import views

app_name = 'api'

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'images', views.ImageViewSet, base_name='UploadFile')

urlpatterns = [
    url(r'', include(router.urls)),
]
