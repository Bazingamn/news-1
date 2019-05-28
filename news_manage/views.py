from django.http import HttpResponse
from news_manage import api as news_manage
# Create your views here.


def get_news_list(request):
    return HttpResponse(news_manage.get_news_list(request), content_type="application/json")


def get_video_list(request):
    return HttpResponse(news_manage.get_video_list(request), content_type="application/json")
