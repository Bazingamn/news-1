from django.shortcuts import render, redirect
from django.http import HttpResponse
from admin_status import api as admin_status
from news import settings
import time


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


def nav_news(request, news_id):
    try:
        mycol = settings.DB_CON['news']
        news_info = list(mycol.find({'_id': int(news_id)}))
        if len(news_info) == 1:
            news_info[0]['timestamp'] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(news_info[0]['timestamp']))
            return render(request, 'news.html', {'news_info': news_info[0]})
        else:
            return render(request, '404.html')
    except Exception as e:
        return render(request, '404.html')


def modify_passwd(request):
    return HttpResponse(admin_status.modify_passwd(request), content_type="application/json")


def get_use_rec(request):
    return HttpResponse(admin_status.get_use_rec(request), content_type="application/json")


def get_regist_rec(request):
    return HttpResponse(admin_status.get_regist_rec(request), content_type="application/json")


def get_hot_news(request):
    return HttpResponse(admin_status.get_hot_news(request), content_type="application/json")


def get_hot_search(request):
    return HttpResponse(admin_status.get_hot_search(request), content_type="application/json")


def get_today_data(request):
    return HttpResponse(admin_status.get_today_data(request), content_type="application/json")


def get_all_data(request):
    return HttpResponse(admin_status.get_all_data(request), content_type="application/json")


def get_use_loc(request):
    return HttpResponse(admin_status.get_use_loc(request), content_type="application/json")
