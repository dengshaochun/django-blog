#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 19:27
# @Author  : Dengsc
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django.forms import ModelForm, TextInput
from app.models import Article


class ArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'body', 'status', 'abstract', 'topped',
                  'category', 'tags')
        widgets = {
            'title': TextInput(attrs={'id': 'local-search-input'}),
            'abstract': TextInput(attrs={'id': 'local-search-input'}),
        }
