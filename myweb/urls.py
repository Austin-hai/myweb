"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from article.views import article_list

urlpatterns = [
    path('admin/', admin.site.urls),

    # home 博客主页
    path('', article_list, name='home'),

    # 新增代码，配置app的url
    path('article/', include('article.urls', namespace='article')),

    # 新增代码，配置app的url
    path('mtu/', include('mtu.urls', namespace='mtu')),

    # 新增代码，配置app的url
    path('friendlink/', include('friendlink.urls', namespace='friendlink')),

    # # 评论
    # path('comment/', include('comment.urls', namespace='comment')),

    # 第三方登录
    path('accounts/', include('allauth.urls')),

    path('mdeditor/', include('mdeditor.urls'))

]# 添加这行
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)