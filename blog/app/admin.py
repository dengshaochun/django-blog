# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import (Profile, Article, Category, Link, Image,
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
    list_display = ('username', 'email', 'created_time')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'location')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'icon', 'type', 'state')


admin.site.register((Tag, Suggest, BlogMeta, Icon, Image))
admin.site.register(Article, ArticleAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Link, LinkAdmin)
