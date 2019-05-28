# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import redirect


try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path != '/login/' and request.path != '/':
            tocken = request.session.get('tocken')
            if tocken:
                request.session['tocken'] = tocken
            else:
                return redirect('/')
