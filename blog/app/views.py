# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render
from app.models import Article, Category, Tag, Profile, BlogComment
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import markdown
import re
import logging

# Create your views here.


logger = logging.getLogger(__name__)


class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    # 制定获取的model数据列表的名字
    context_object_name = "article_list"

    def get_queryset(self):
        """
        过滤数据，获取已发布文章列表，并转为html格式
        Returns:
        """
        article_list = Article.objects.filter(status='p')
        return article_list


class ArticleDetailView(DetailView):
    """
    显示文章详情
    """
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = "article"

    # pk_url_kwarg用于接受来自url中的参数作为主键
    pk_url_kwarg = 'article_id'

    # 从数据库中获取id为pk_url_kwargs的对象
    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        # 点击一次阅读量增加一次
        obj.views += 1
        obj.save()
        obj.body = markdown.markdown(obj.body, safe_mode='escape',
                                     extensions=[
                                        'markdown.extensions.toc',
                                        'markdown.extensions.sane_lists',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.abbr',
                                        'markdown.extensions.attr_list',
                                        'markdown.extensions.def_list',
                                        'markdown.extensions.fenced_code',
                                        'markdown.extensions.footnotes',
                                        'markdown.extensions.smart_strong',
                                        'markdown.extensions.meta',
                                        'markdown.extensions.nl2br',
                                        'markdown.extensions.tables'
                                        ])
        return obj

    # 新增form到上下文
    def get_context_data(self, **kwargs):
        kwargs['comments'] = self.object.blogcomment_set.all()
        kwargs['tags'] = self.object.tags.all()
        return super(ArticleDetailView, self).get_context_data(**kwargs)


class AboutView(DetailView):

    model = Profile
    template_name = 'blog/about.html'

    def get_object(self, queryset=None):
        pass

    def get_context_data(self, **kwargs):
        return super(AboutView, self).get_context_data(**kwargs)


class CategoryView(DetailView):

    model = Category
    template_name = 'blog/categories.html'

    def get_object(self, queryset=None):
        pass

    def get_context_data(self, **kwargs):
        return super(CategoryView, self).get_context_data(**kwargs)


class TagView(DetailView):

    model = Tag
    template_name = 'blog/tags.html'

    def get_object(self, queryset=None):
        pass

    def get_context_data(self, **kwargs):
        return super(TagView, self).get_context_data(**kwargs)


class ArchiveView(DetailView):

    model = Article
    template_name = 'blog/archives.html'

    def get_object(self, queryset=None):
        pass

    def get_context_data(self, **kwargs):
        return super(ArchiveView, self).get_context_data(**kwargs)
