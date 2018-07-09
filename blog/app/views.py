# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from app.models import (Article, Category, Tag, BlogMeta, Link)
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from app.forms import CommentForm
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

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
        article_list = Article.objects.filter(status='p')
        return article_list

    def get_context_data(self, **kwargs):
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(CustomDetailView):

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

    def get_comments(self):
        comments = []
        comment_list = []
        comment_list_dict = {}
        for row in self.object.blogcomment_set.all():
            comment = model_to_dict(row)
            comment.update({'children': []})
            comment_list.append(comment)
            comment_list_dict[comment['id']] = comment

        for item in comment_list:
            parent_row = comment_list_dict.get(item['parent_comment'])
            if not parent_row:
                comments.append(item)
            else:
                parent_row['children'].append(item)
        return comments

    # 新增form到上下文
    def get_context_data(self, **kwargs):
        kwargs['comments'] = self.get_comments()
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
                'pk': category.pk,
                'name': category.name,
                'count': category.article_set.filter(status='p').count()
            })
        return category_list

    def get_context_data(self, **kwargs):
        return super(CategoryView, self).get_context_data(**kwargs)


class CategoryDetailView(CustomListView):

    model = Category
    template_name = 'blog/filter.html'
    context_object_name = 'article_list'

    def get_queryset(self, queryset=None):
        category = Category.objects.get(pk=self.kwargs.get('category'))
        if category:
            return category.article_set.filter(
                status='p').order_by('-created_time').all()
        else:
            return []

    def get_context_data(self, **kwargs):
        kwargs['filter'] = Category.objects.get(
            pk=self.kwargs.get('category')).name
        return super(CategoryDetailView, self).get_context_data(**kwargs)


class TagView(CustomListView):

    model = Tag
    template_name = 'blog/tags.html'
    context_object_name = 'tag_list'

    def get_queryset(self, queryset=None):
        tag_list = []
        tags = Tag.objects.all()
        for tag in tags:
            tag_list.append({
                'pk': tag.pk,
                'name': tag.name,
                'count': tag.article_set.filter(status='p').count()
            })
        return tag_list

    def get_context_data(self, **kwargs):
        return super(TagView, self).get_context_data(**kwargs)


class TagDetailView(CustomListView):

    model = Tag
    template_name = 'blog/filter.html'
    context_object_name = 'article_list'

    def get_queryset(self, queryset=None):
        tag = Tag.objects.get(pk=self.kwargs.get('tag'))
        if tag:
            return tag.article_set.filter(
                status='p').order_by('-created_time').all()
        else:
            return []

    def get_context_data(self, **kwargs):
        kwargs['filter'] = Tag.objects.get(
            pk=self.kwargs.get('tag')).name
        return super(TagDetailView, self).get_context_data(**kwargs)


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


class BlogCommentView(FormView):
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        target_article = get_object_or_404(Article,
                                           pk=self.kwargs['article_id'])
        comment = form.save(commit=False)
        comment.article = target_article
        self.success_url = target_article.get_absolute_url()
        return redirect(reverse('blog:articles',
                                args=(self.kwargs['article_id'])))

    def form_invalid(self, form):
        target_article = get_object_or_404(Article,
                                           pk=self.kwargs['article_id'])
        return render(self.request, 'blog/detail.html', {
            'form': form,
            'article': target_article,
            'comment_list': target_article.blogcomment_set.all(),
        })

