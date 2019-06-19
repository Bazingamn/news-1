from django.http import HttpResponse
from news_manage import api as news_manage
# Create your views here.


def get_news_list(request):
    return HttpResponse(news_manage.get_news_list(request), content_type="application/json")


def get_video_list(request):
    return HttpResponse(news_manage.get_video_list(request), content_type="application/json")


def get_recommend_list(request):
    return HttpResponse(news_manage.get_recommend_list(request), content_type="application/json")


def get_type_list(request):
    return HttpResponse(news_manage.get_type_list(request), content_type="application/json")


def get_news_detail(request):
    return HttpResponse(news_manage.get_news_detail(request), content_type="application/json")


def collect_news(request):
    return HttpResponse(news_manage.collect_news(request), content_type="application/json")


def check_collect(request):
    return HttpResponse(news_manage.check_collect(request), content_type="application/json")


def search_news(request):
    return HttpResponse(news_manage.search_news(request), content_type="application/json")


def get_collect_news(request):
    return HttpResponse(news_manage.get_collect_news(request), content_type="application/json")


def delete_collect_news(request):
    return HttpResponse(news_manage.delete_collect_news(request), content_type="application/json")


def delete_all_collect(request):
    return HttpResponse(news_manage.delete_all_collect(request), content_type="application/json")


def get_comment(request):
    return HttpResponse(news_manage.get_comment(request), content_type="application/json")


def delete_comment(request):
    return HttpResponse(news_manage.delete_comment(request), content_type="application/json")


def delete_all_comment(request):
    return HttpResponse(news_manage.delete_all_comment(request), content_type="application/json")


def get_news_comment(request):
    return HttpResponse(news_manage.get_news_comment(request), content_type="application/json")


def add_comment(request):
    return HttpResponse(news_manage.add_comment(request), content_type="application/json")
