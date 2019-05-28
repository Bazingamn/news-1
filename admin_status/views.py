from django.shortcuts import render, redirect
from django.http import HttpResponse
from admin_status import api as admin_status


def index(request):
    return render(request, 'index.html')


def login(request):
    return HttpResponse(admin_status.login(request), content_type="application/json")


def logout(request):
    del request.session['tocken']
    return redirect('/')


def menu(request):
    print(request.session.get('tocken'))
    return render(request, 'menu.html')


def to_url(request, file_name):
    return render(request, file_name + '.html')


def modify_passwd(request):
    return HttpResponse(admin_status.modify_passwd(request), content_type="application/json")
