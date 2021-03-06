#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/20 20:47
# @Author  : Dengsc
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django.forms import (Form, fields, widgets, ModelForm, TextInput,
                          Select, SelectMultiple, CheckboxInput, Textarea)
from app.models import Article


class LoginForm(Form):
    username = fields.CharField(
        required=True,
        widget=widgets.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Username'
                   }),
        strip=True,
        error_messages={'required': '用户名不能为空', }
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Username',
                   'type': 'password'
                   }),
        required=True,
        strip=True,
        error_messages={'required': '密码不能为空!', }
    )


class ArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'body', 'status', 'abstract', 'topped',
                  'category', 'tags')
        widgets = {
            'title': TextInput(attrs={
                'class':
                    'form-control col-md-7 col-xs-12'
            }),
            'abstract': TextInput(attrs={
                'class':
                    'form-control col-md-7 col-xs-12'
            }),
            'status': Select(attrs={
                'class': 'form-control'
            }),
            'topped': CheckboxInput(attrs={
                'class': 'js-switch'
            }),
            'tags': SelectMultiple(attrs={
                'class': 'select2_multiple form-control'
            }),
            'category': Select(attrs={
                'class': 'form-control'
            }),
            'body': Textarea()
        }
