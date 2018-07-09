#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 19:27
# @Author  : Dengsc
# @Site    : 
# @File    : forms.py
# @Software: PyCharm


from app.models import BlogComment
from django.forms import ModelForm, TextInput, Textarea


class CommentForm(ModelForm):

    class Meta:
        model = BlogComment
        fields = ('username', 'email', 'private_url', 'body')

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入昵称',
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入邮箱',
            }),
            'private_url': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '个人博客地址<我相信不是广告>'
            }),
            'body': Textarea(attrs={'placeholder': '我来评两句~'}),
        }