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
    url(r'^tags/(?P<tag>\d+)/$', views.TagDetailView.as_view(),
        name='tag-detail'),
    url(r'^tags/$', views.TagView.as_view(), name='tag-list'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^archives/$', views.ArchiveView.as_view(), name='archive-list'),
    url(r'^categories/(?P<category>\d+)/$', views.CategoryDetailView.as_view(),
        name='category-detail'),
    url(r'^categories/$', views.CategoryView.as_view(), name='category-list'),
    url(r'^articles/(?P<article_id>\d+)/$',
        cache_page(60 * 15)(views.ArticleDetailView.as_view()),
        name='article-detail'),
    url(r'^articles/$', views.IndexView.as_view(), name='article-list')
]
