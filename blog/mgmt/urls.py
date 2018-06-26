#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/20 20:51
# @Author  : Dengsc
# @Site    : 
# @File    : urls.py
# @Software: PyCharm


from django.conf.urls import url
from mgmt import views

app_name = 'mgmt'

urlpatterns = [
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^images/$', views.UploadImageView.as_view(), name='images'),
    url(r'^editor/$', views.EditorView.as_view(), name='editor'),
]
