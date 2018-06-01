# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from app.models import (Article, Category, Tag,
                        BlogComment, BlogMeta, Link)
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import markdown
import logging

# Create your views here.


logger = logging.getLogger(__name__)


def get_common_kwargs(**kwargs):
    kwargs['blog_meta'] = BlogMeta.objects.get(pk=1)
    kwargs['article_count'] = Article.objects.count()
    kwargs['category_count'] = Category.objects.count()
    kwargs['tag_count'] = Tag.objects.count()
    kwargs['private_links'] = Link.objects.filter(
        state=True).filter(type=0).all()
    kwargs['friendly_links'] = Link.objects.filter(
        state=True).filter(type=1).all()
    return kwargs


class CustomListView(ListView):

    def get_context_data(self, **kwargs):
        kwargs = get_common_kwargs(**kwargs)
        return super(CustomListView, self).get_context_data(**kwargs)


class CustomDetailView(DetailView):

    def get_context_data(self, **kwargs):
        kwargs = get_common_kwargs(**kwargs)
        return super(CustomDetailView, self).get_context_data(**kwargs)


class IndexView(CustomListView):
    model = Article
    template_name = 'blog/index.html'
    # 制定获取的model数据列表的名字
    context_object_name = 'article_list'

    def get_queryset(self):
        """
        过滤数据，获取已发布文章列表，并转为html格式
        Returns:
        """
        article_list = Article.objects.filter(status='p')
        return article_list

    def get_context_data(self, **kwargs):
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(CustomDetailView):
    """
    显示文章详情
    """
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

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
                                        'markdown.extensions.extra',
                                        'markdown.extensions.abbr',
                                        'markdown.extensions.attr_list',
                                        'markdown.extensions.def_list',
                                        'markdown.extensions.fenced_code',
                                        'markdown.extensions.footnotes',
                                        'markdown.extensions.tables',
                                        'markdown.extensions.smart_strong',
                                        'markdown.extensions.admonition',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.headerid',
                                        'markdown.extensions.meta',
                                        'markdown.extensions.nl2br',
                                        'markdown.extensions.sane_lists',
                                        'markdown.extensions.smarty',
                                        'markdown.extensions.wikilinks'
                                        ])
        return obj

    # 新增form到上下文
    def get_context_data(self, **kwargs):
        kwargs['comments'] = self.object.blogcomment_set.all()
        kwargs['tags'] = self.object.tags.all()
        kwargs['prev_article'] = Article.objects.filter(
            pk=self.object.pk - 1).first()
        kwargs['next_article'] = Article.objects.filter(
            pk=self.object.pk + 1).first()
        return super(ArticleDetailView, self).get_context_data(**kwargs)


class AboutView(CustomDetailView):

    model = BlogMeta
    template_name = 'blog/about.html'
    context_object_name = 'blog_meta'

    def get_object(self, queryset=None):
        return BlogMeta.objects.get(pk=1)

    def get_context_data(self, **kwargs):
        return super(AboutView, self).get_context_data(**kwargs)


class CategoryView(CustomListView):

    model = Category
    template_name = 'blog/categories.html'
    context_object_name = 'category_list'

    def get_queryset(self, queryset=None):
        category_list = []
        categories = Category.objects.all()
        for category in categories:
            category_list.append({
                'name': category.name,
                'count': Article.objects.filter(category=category).count()
            })
        return category_list

    def get_context_data(self, **kwargs):
        return super(CategoryView, self).get_context_data(**kwargs)


class TagView(CustomListView):

    model = Tag
    template_name = 'blog/tags.html'
    context_object_name = 'tag_list'

    def get_queryset(self, queryset=None):
        tag_list = []
        tags = Tag.objects.all()
        for tag in tags:
            tag_list.append({
                'name': tag.name,
                'count': tag.article_set.count()
            })
        return tag_list

    def get_context_data(self, **kwargs):
        return super(TagView, self).get_context_data(**kwargs)


class ArchiveView(CustomListView):

    model = Article
    template_name = 'blog/archives.html'
    context_object_name = 'article_list'

    def get_queryset(self, queryset=None):

        article_list = Article.objects.filter(
            status='p').order_by('-created_time')
        return article_list

    def get_context_data(self, **kwargs):
        return super(ArchiveView, self).get_context_data(**kwargs)


class EditorView(CustomDetailView):

    model = Article
    template_name = 'blog/editor.html'

    def get_object(self, queryset=None):
        return None

    def get_context_data(self, **kwargs):
        return super(EditorView, self).get_context_data(**kwargs)
