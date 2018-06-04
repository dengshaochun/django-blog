#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/28 19:43
# @Author  : Dengsc
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from django.views.decorators.cache import cache_page
from app import views

app_name = 'app'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url('^tags/', views.TagView.as_view(), name='tags'),
    url('^images/', views.upload_image, name='images'),
    url('^editor/', views.EditorView.as_view(), name='editor'),
    url('^about/', views.AboutView.as_view(), name='about'),
    url('^archives/', views.ArchiveView.as_view(), name='archives'),
    url('^categories/', views.CategoryView.as_view(), name='categories'),
    url(r'^article/(?P<article_id>\d+)$',
        cache_page(60 * 15)(views.ArticleDetailView.as_view()), name='detail'),
]
