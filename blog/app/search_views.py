#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/22 20:55
# @Author  : Dengsc
# @Site    : 
# @File    : search_views.py.py
# @Software: PyCharm


from haystack.views import SearchView
from app.models import BlogMeta, Article, Category, Tag, Link


class MySeachView(SearchView):
    def extra_context(self):  # 重载extra_context来添加额外的context内容
        context = super(MySeachView, self).extra_context()
        context['blog_meta'] = BlogMeta.objects.get(pk=1)
        context['article_count'] = Article.objects.count()
        context['category_count'] = Category.objects.count()
        context['tag_count'] = Tag.objects.count()
        context['private_links'] = Link.objects.filter(
            state=True).filter(type=0).all()
        context['friendly_links'] = Link.objects.filter(
            state=True).filter(type=1).all()
        return context
