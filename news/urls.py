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
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', admin_status.index),
    path('login/', admin_status.login),
    path(r'menu/<file_name>.html', admin_status.to_url),
    path(r'menu/', admin_status.menu),
    path(r'menu/modifyPasswd/', admin_status.modify_passwd),
    path(r'menu/logout/', admin_status.logout),
    path('getNewsList/', news_manage.get_news_list),
    path('getVideoList/', news_manage.get_video_list),
]
