#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/20 20:51
# @Author  : Dengsc
# @Site    : 
# @File    : urls.py
# @Software: PyCharm


from django.conf.urls import url
from management import views

app_name = 'management'

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
]
