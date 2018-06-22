#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/22 19:48
# @Author  : Dengsc
# @Site    : 
# @File    : search_indexes.py.py
# @Software: PyCharm


import datetime
from haystack import indexes
from app.models import Article


# 类名必须为需要检索的Model_name+Index，这里需要检索Article，所以创建ArticleIndex
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)  # 创建一个text字段
    author = indexes.CharField(model_attr='author')  # 创建一个author字段
    created_time = indexes.DateTimeField(model_attr='created_time')

    def get_model(self):  # 重载get_model方法，必须要有！
        return Article

    def index_queryset(self, using=None):  # 重载index_..函数
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(
            created_time__lte=datetime.datetime.now())
