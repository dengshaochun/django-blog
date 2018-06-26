# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from mgmt.forms import LoginForm, ArticleForm
from django.contrib.auth import login, authenticate, logout
from app.models import BlogMeta, Image
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse

# Create your views here.


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('mgmt:index'))
        form = LoginForm()
        return render(request, 'mgmt/login.html', {'form': form})

    def post(self, request):
        f = LoginForm(request.POST)
        if f.is_valid():
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user.is_active and user.is_superuser:
                login(request, user)
                return redirect(reverse('mgmt:index'))
            else:
                return render(request, 'mgmt/login.html', {'form': f})
        return render(request, 'mgmt/login.html', {'form': f})


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'mgmt/index.html')


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect(reverse('mgmt:login'))


class EditorView(LoginRequiredMixin, View):

    def get(self, request):
        blog_meta = BlogMeta.objects.get(pk=1)
        form = ArticleForm()
        return render(request, 'mgmt/editor.html',
                      {'form': form,
                       'blog_meta': blog_meta
                       }
                      )

    def post(self, request):
        f = ArticleForm(request.POST)
        new_article = f.save(commit=False)
        new_article.author = request.user
        new_article.save()
        return redirect(reverse('mgmt:index'))


@method_decorator(csrf_exempt, name='dispatch')
class UploadImageView(LoginRequiredMixin, View):
    data = {
        'success': 0,
        'message': '',
        'url': ''
    }

    def post(self, request):
        new_img = Image(
            image=request.FILES.get('editormd-image-file'),
        )
        new_img.save()
        self.data['success'] = 1
        self.data['url'] = new_img.image.url
        return JsonResponse(self.data)
