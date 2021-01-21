# 导入数据模型ArticlePost
from django.views.generic.base import View
from .models import ArticlePost, ArticleColumn
from taggit.managers import TaggableManager

# 引入分页模块
from django.core.paginator import Paginator
# 引入 Q 对象
from django.db.models import Q
# 引入redirect重定向模块
from django.shortcuts import render, redirect, get_object_or_404
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
# 引入markdown模块
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.decorators.clickjacking import xframe_options_sameorigin
# from comment.models import Article_comment


def article_list(request):
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    article_tags = request.GET.get('article_tags')
    excerpt = request.GET.get('excerpt')

    # 初始化查询集
    articlelist = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        # 用 Q对象 进行联合搜索
        articlelist = articlelist.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        # 将 search 参数重置为空
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        articlelist = articlelist.filter(column=column)

    # 摘要查询集
    if excerpt and excerpt != 'None':
        articlelist = articlelist.filter(excerpt=excerpt)

    # 标签查询集
    if article_tags and article_tags != 'None':
        articlelist = articlelist.filter(tags__name__in=[article_tags])

    # 查询集排序
    if order == 'total_views':
        articlelist = articlelist.order_by('-total_views')

    # 每页显示 6 篇文章
    paginator = Paginator(articlelist, 6)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {'articles': articles, 'excerpt': excerpt, 'order': order, 'search': search,
               'column': column, 'article_tags': article_tags,
               }
    # render函数：载入模板，并返回context对象
    return render(request, 'article/home_index.html', context)


class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')


# 文章详情
@ xframe_options_sameorigin
def article_detail(request, id):
    # 取出相应的文章
    article = get_object_or_404(ArticlePost, id=id)

    # # 取出文章评论
    # comments = Article_comment.objects.filter(article=id)

    # 过滤出所有的id比当前文章小的文章
    pre_article = ArticlePost.objects.filter(id__lt=article.id).order_by('-id')
    # 过滤出id大的文章
    next_article = ArticlePost.objects.filter(id__gt=article.id).order_by('id')

    # 取出相邻前一篇文章
    if pre_article.count() > 0:
        pre_article = pre_article[0]
    else:
        pre_article = None

    # 取出相邻后一篇文章
    if next_article.count() > 0:
        next_article = next_article[0]
    else:
        next_article = None

    # 将markdown语法渲染成html样式
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 修改 Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify),
        ]
    )
    article.body = md.convert(article.body)


    # 需要传递给模板的对象
    # 新增了md.toc对象
    context = {'article': article, 'toc': md.toc,
               'pre_article': pre_article,
               'next_article': next_article,
               }
    # 载入模板，并返回context对象
    return render(request, 'article/article_detail.html', context)


# 写文章的视图
@ xframe_options_sameorigin
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=1)
            # 将新文章保存到数据库中
            new_article.save()
            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/article_create.html', context)


def archive(request, year, month):

    articles_year = ArticlePost.objects.filter(created__year=year).order_by('-created')
    year_list = ArticlePost.objects.dates('created', 'year', order='DESC')

    articles_month = articles_year.filter(created__month=month).order_by('-created')
    month_list = ArticlePost.objects.dates('created', 'month', order='DESC')
    context = {'articles_year': articles_year, 'year_list': year_list,
               'articles_month': articles_month,
               'month_list': month_list,
               }

    return render(request, 'article/archives_list.html', context)


def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(ArticleColumn, pk=pk)
    articles = ArticlePost.objects.filter(column=cate).order_by('-created')
    # 每页显示 6 篇文章
    paginator = Paginator(articles, 6)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    return render(request, 'article/home_index.html', context={'articles': articles})


def tag(request, pk):
    # 记得在开始部分导入 Tag 类

    tags = ArticlePost.article_tags.all()
    t = get_object_or_404(tags, pk=pk)
    articles = ArticlePost.objects.filter(article_tags__name__in=[t]).order_by('-created')
    # 每页显示 6 篇文章
    paginator = Paginator(articles, 6)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    return render(request, 'article/home_index.html', context={'articles': articles})


def about(request):
    # 记得在开始部分导入 Tag 类
    return render(request, 'article/about_me.html')


def timeline(request):
    # 记得在开始部分导入 Tag 类
    return render(request, 'article/timeline.html')
