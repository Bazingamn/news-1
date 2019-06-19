# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import redirect


try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

NO_LOGIN_URLS = ['/getVideoList/',
                 '/getNewsList/', '/login/', '/', '/getTypeList/', '/getNewsDetail/', '/collectNews/', '/getCollectRec/']


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(request.path)
        if '/web' in request.path and request.path != '/web/login/':
            tocken = request.session.get('tocken')
            if tocken:
                request.session['tocken'] = tocken
            else:
                return redirect('/')
