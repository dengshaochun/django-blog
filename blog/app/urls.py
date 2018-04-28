#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/28 19:43
# @Author  : Dengsc
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]
