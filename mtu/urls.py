from django.urls import path
from . import views

# 正在部署的应用的名称
app_name = 'mtu'

urlpatterns = [
    # 目前还没有urls
    path('homepage/', views.Index, name='homepage'),

    path('institution-list/', views.Institution_list, name='institution_list'),

    path('institution-info/<int:id>/', views.institution_detail, name='institution-info'),

    path('goddess-list/', views.GoddessListView.as_view(), name='goddess_list'),

    path('goddess-ranking/', views.GoddessrankingListView.as_view(), name='goddess_ranking'),

    path('goddess_info/<int:id>/', views.goddess_detail, name='goddess_info'),

    path('album-list/', views.AlbumListView.as_view(), name='album_list'),

    path('album_info/<int:id>/', views.album_detail, name='album_info'),

    path('tagcloud/', views.tagcloud, name='tagcloud'),

    path('alltags/<int:pk>/', views.alltag, name='alltag'),

    path('style/<int:pk>/', views.style, name='style'),

]