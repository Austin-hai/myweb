from . import views
# 引入path
from django.urls import path
# 正在部署的应用的名称
app_name = 'friendlink'


urlpatterns = [

    # path函数将url映射到视图web_link
    path('weblink', views.Web_index, name='weblink'),

    # path函数将url映射到视图web_link
    path('friend', views.friend_linkListView.as_view(), name='friend'),

]