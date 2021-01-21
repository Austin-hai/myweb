from django.contrib import admin

# 别忘了导入ArticlerPost
from .models import ArticlePost
from .models import ArticleColumn
# 自定义管理站点的名称和URL标题
admin.site.site_header = 'Austin Backend'
admin.site.site_title = 'Austin后台管理'


@admin.register(ArticlePost)
class ArticlePostAdmin(admin.ModelAdmin):
    # 这个的作用是给出一个筛选机制，一般按照时间比较好
    date_hierarchy = 'created'

    exclude = ('total_views',)

    # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
    list_display = ('id', 'column', 'title', 'author', 'created', 'updated')

    # 设置需要添加<a>标签的字段
    list_display_links = ('title',)

    # 激活过滤器，这个很有用
    list_filter = ('column', 'created',)

    list_per_page = 50  # 控制每页显示的对象数量，默认是100

    # 限制用户权限，只能看到自己编辑的文章
    def get_queryset(self, request):
        qs = super(ArticlePostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


# 注册文章栏目
admin.site.register(ArticleColumn)
