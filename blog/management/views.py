# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from management.forms import LoginForm
from django.contrib.auth import login, authenticate

# Create your views here.


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'management/login.html', {'form': form})

    def post(self, request):
        f = LoginForm(request.POST)
        print f.is_valid()
        print f.errors
        if f.is_valid():
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user.is_active and user.is_superuser:
                login(request, user)
                return redirect(reverse('management:index'))
            else:
                return render(request, 'management/login.html', {'form': f})
        return render(request, 'management/login.html', {'form': f})


class IndexView(View):

    def get(self, request):
        return render(request, 'management/index.html')
