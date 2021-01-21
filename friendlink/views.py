from django.views.generic import ListView
from .models import Link_type, Friend_link
# 引入redirect重定向模块
from django.shortcuts import render, redirect, get_object_or_404


def Web_index(request):

    mediums = Friend_link.objects.filter(link_type__title__exact="影音视频")

    books = Friend_link.objects.filter(link_type__title__exact="阅读学习")

    tools = Friend_link.objects.filter(link_type__title__exact="常用工具")

    works = Friend_link.objects.filter(link_type__title__exact="日常办公")

    pics = Friend_link.objects.filter(link_type__title__exact="图库壁纸")

    webs = Friend_link.objects.filter(link_type__title__exact="个人网站")

    fu_lis = Friend_link.objects.filter(link_type__title__exact="福利")

    # 需要传递给模板（templates）的对象
    context = {'mediums': mediums, 'books': books, 'tools': tools, 'works': works,
               'pics': pics, 'webs': webs, 'fu_lis': fu_lis,
               }
    # render函数：载入模板，并返回context对象
    return render(request, 'friendlink/link_index.html', context)


class friend_linkListView(ListView):
    # 上下文的名称
    context_object_name = 'friends'
    # 查询集
    queryset = Friend_link.objects.filter(link_type__title__exact="友人帐")
    # 模板位置
    template_name = 'friendlink/friend_link.html'