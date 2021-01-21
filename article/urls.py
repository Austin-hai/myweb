from . import views
# 引入path
from django.urls import path
# 正在部署的应用的名称
app_name = 'article'


urlpatterns = [
    # path函数将url映射到视图
    # path('article-list/', views.article_list, name='article_list'),

    # 文章详情
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),

    # 写文章
    path('article-create/', views.article_create, name='article_create'),

    # 文章归档
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),

    path('categories/<int:pk>/', views.category, name='category'),

    path('tags/<int:pk>/', views.tag, name='tag'),



    # 点赞 +1
    path('increase-likes/<int:id>/', views.IncreaseLikesView.as_view(), name='increase_likes'),

    # 关于我
    path('about/', views.about, name='about'),

    # 时间线
    path('timeline/', views.timeline, name='timeline'),

]