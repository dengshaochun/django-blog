#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/28 19:43
# @Author  : Dengsc
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^article/(?P<article_id>\d+)$',
        cache_page(60 * 15)(views.ArticleDetailView.as_view()), name='detail'),
]
