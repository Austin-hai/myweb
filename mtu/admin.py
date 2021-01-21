from django.contrib import admin
# 自定义管理站点的名称和URL标题
admin.site.site_header = 'Austin Backend'
admin.site.site_title = 'Austin后台管理'
from django.contrib.auth.models import User

from .models import Album
from .models import Image
from .models import Goddess, Institution
from taggit.managers import TaggableManager


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    # 这个的作用是给出一个筛选机制，一般按照时间比较好
    date_hierarchy = 'created'

    # exclude = ('total_views',)

    # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
    list_display = ('id', 'title', 'artist', 'created')

    # 设置需要添加<a>标签的字段
    list_display_links = ('title',)

    # 激活过滤器，这个很有用
    list_filter = ('created', 'artist')

    list_per_page = 50  # 控制每页显示的对象数量，默认是100

    # 限制用户权限，只能看到自己编辑的文章
    def get_queryset(self, request):
        qs = super(AlbumAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


@admin.register(Goddess)
class GoddessAdmin(admin.ModelAdmin):
    # 这个的作用是给出一个筛选机制，一般按照时间比较好
    date_hierarchy = 'created'

    # exclude = ('total_views',)

    search_fields = ['artist_name']

    # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
    list_display = ('id', 'artist_name', 'ranking', 'hometown', 'birthday', 'body_bra', 'body_butt', 'created')

    # 设置需要添加<a>标签的字段
    list_display_links = ('artist_name',)

    # 激活过滤器，这个很有用
    list_filter = ('created', 'artist_name', 'body_bra', 'hometown', 'birthday')

    list_per_page = 50  # 控制每页显示的对象数量，默认是100

    # 限制用户权限，只能看到自己编辑的文章
    def get_queryset(self, request):
        qs = super(GoddessAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    # 这个的作用是给出一个筛选机制，一般按照时间比较好

    search_fields = ['institution_name', 'style']

    # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
    list_display = ('id', 'institution_name', 'description', 'style', 'created')

    # 设置需要添加<a>标签的字段
    list_display_links = ('institution_name',)

    # 激活过滤器，这个很有用
    list_filter = ('created', 'institution_name', 'style')

    list_per_page = 50  # 控制每页显示的对象数量，默认是100

    # 限制用户权限，只能看到自己编辑的文章
    def get_queryset(self, request):
        qs = super(InstitutionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


admin.site.register(Image)