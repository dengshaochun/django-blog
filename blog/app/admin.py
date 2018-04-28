# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import Profile, Article, Category, BlogComment, Tag, Suggest

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.readonly_fields = ('author',)
        self.filter_horizontal = ('tags', )
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        return form


class BlogCommentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.readonly_fields = ('user',)
        form = super(BlogCommentAdmin, self).get_form(request, obj, **kwargs)
        return form

admin.site.register((Profile, Category, Tag, Suggest))
admin.site.register(Article, ArticleAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
