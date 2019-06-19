from django.shortcuts import render, HttpResponse
from user_manage import api as user_manage

# Create your views here.


def sign_up(request):
    return HttpResponse(user_manage.sign_up(request), content_type="application/json")


def modify_user_info(request):
    return HttpResponse(user_manage.modify_user_info(request), content_type="application/json")


def modify_logo(request):
    return HttpResponse(user_manage.modify_logo(request), content_type="application/json")


def send_check_code(request):
    return HttpResponse(user_manage.send_check_code(request), content_type="application/json")


def login(request):
    return HttpResponse(user_manage.login(request), content_type="application/json")
