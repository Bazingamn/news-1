"""news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from news_manage import views as news_manage
from admin_status import views as admin_status
from user_manage import views as user_manage
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', admin_status.index),
    path('news/<news_id>', admin_status.nav_news),
    path('web/login/', admin_status.login),
    path(r'web/<file_name>.html', admin_status.to_url),
    path(r'web/menu/', admin_status.menu),
    path(r'web/modifyPasswd/', admin_status.modify_passwd),
    path(r'web/menu/logout/', admin_status.logout),
    path(r'web/getUseRec/', admin_status.get_use_rec),
    path(r'web/getRegistRec/', admin_status.get_regist_rec),
    path(r'web/getUseLoc/', admin_status.get_use_loc),
    path('web/getHotNews/', admin_status.get_hot_news),
    path('web/getHotSearch/', admin_status.get_hot_search),
    path('web/getTodayData/', admin_status.get_today_data),
    path('web/getAllData/', admin_status.get_all_data),
    path('app/getNewsList/', news_manage.get_news_list),
    path('app/getVideoList/', news_manage.get_video_list),
    path('app/getRecommendList/', news_manage.get_recommend_list),
    path('app/getTypeList/', news_manage.get_type_list),
    path('app/getNewsDetail/', news_manage.get_news_detail),
    path('app/collectNews/', news_manage.collect_news),
    path('app/searchNews/', news_manage.search_news),
    path('app/getCollectRec/', news_manage.get_collect_news),
    path('app/deleteCollectRec/', news_manage.delete_collect_news),
    path('app/checkCollect/', news_manage.check_collect),
    path('app/deleteAllCollect/', news_manage.delete_all_collect),
    path('app/getComment/', news_manage.get_comment),
    path('app/deleteComment/', news_manage.delete_comment),
    path('app/deleteAllComment/', news_manage.delete_all_comment),
    path('app/getNewsComment/', news_manage.get_news_comment),
    path('app/addComment/', news_manage.add_comment),
    path('app/sendCheckCode/', user_manage.send_check_code),
    path('app/signUp/', user_manage.sign_up),
    path('app/modifyUserInfo/', user_manage.modify_user_info),
    path('app/modifyLogo/', user_manage.modify_logo),
    path('app/logIn/', user_manage.login),
]
