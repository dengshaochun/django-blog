# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import (Profile, Article, Category, FriendlyLink,
                        BlogComment, Tag, Suggest, BlogMeta, Icon)

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_time')

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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'location')


class FriendlyLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'icon', 'type', 'state')


admin.site.register((Tag, Suggest, BlogMeta, Icon))
admin.site.register(Article, ArticleAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(FriendlyLink, FriendlyLinkAdmin)
