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
        print 'post'
        f = LoginForm(request.POST)
        print f.is_valid()
        print f.errors
        if f.is_valid():
            print 'xxx'
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user.is_active and user.is_superuser:
                print 'pppp'
                login(request, user)
                return redirect(reverse('app:index'))
            else:
                print 'ccc'
                return render(request, 'management/login.html', {'form': f})
        return render(request, 'management/login.html', {'form': f})
