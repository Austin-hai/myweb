from django.shortcuts import render

# Create your views here.
from django.core.checks import register
from django.http import HttpResponse
from django.shortcuts import render
# 引入分页模块
from django.core.paginator import Paginator
# 导入数据模型ArticlePost
# 引入 Q 对象
from django.db.models import Q

from .models import Album
from .models import Image
from .models import Goddess, Institution
from taggit.managers import TaggableManager
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.db.models.aggregates import Count


def Index(request):
    # 取出相应的文章
    goddesses = Goddess.objects.all()[:10:1]
    albums = Album.objects.all()[:10:1]
    context = {"goddesses": goddesses,
               "albums": albums
               }
    return render(request, 'mtu/homepage.html', context)


def Institution_list(request):
    # 查询集
    # queryset = Goddess.objects.all()
    institutions = Institution.objects.annotate(num_albums=Count('album')).filter(num_albums__gt=0)
    context = {"institutions": institutions,
               }
    return render(request, 'mtu/institution_list.html', context)


def institution_detail(request, id):
    # 取出相应的文章
    institution = Institution.objects.get(id=id)
    albums = Album.objects.filter(institution_id=id)
    context = {"institution": institution,
               "albums": albums
               }
    return render(request, 'mtu/institution_info.html', context)





class GoddessListView(ListView):
    # 上下文的名称
    context_object_name = 'goddesses'
    # 查询集
    queryset = Goddess.objects.all()
    paginate_by = 20
    # 模板位置
    template_name = 'mtu/goddess_list.html'


class AlbumListView(ListView):
    # 上下文的名称
    context_object_name = 'albums'
    # 查询集
    queryset = Album.objects.all()
    paginate_by = 30
    # 模板位置
    template_name = 'mtu/album_list.html'


class GoddessrankingListView(ListView):
    # 上下文的名称
    context_object_name = 'goddesses'
    # 查询集
    queryset = Goddess.objects.all()
    # 模板位置
    template_name = 'mtu/goddess_rank.html'


def goddess_detail(request, id):
    # 取出相应的文章
    goddess = Goddess.objects.get(id=id)
    goddess_albums = Album.objects.filter(artist_id=id)
    context = {"goddess": goddess,
               "goddess_albums": goddess_albums
               }
    return render(request, 'mtu/goddess_info.html', context)


def album_detail(request, id):
    # album = get_object_or_404(Goddess, pk=id)
    # return render(request, 'mtu/album_info.html', {"album": album})
    # 取出相应的文章
    pics_list = Image.objects.filter(album_id=id)

    # 每页显示 1 篇文章
    paginator = Paginator(pics_list, 1)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    pics = paginator.get_page(page)

    album = Album.objects.get(id=id)
    refer_albums = Album.objects.all()[:5:1]
    # 过滤出所有的id比当前文章小的文章
    pre_album = Album.objects.filter(id__lt=album.id).order_by('-id')
    # 过滤出id大的文章
    next_album = Album.objects.filter(id__gt=album.id).order_by('id')

    # 取出相邻前一篇文章
    if pre_album.count() > 0:
        pre_album = pre_album[0]
    else:
        pre_album = None

    # 取出相邻后一篇文章
    if next_album.count() > 0:
        next_album = next_album[0]
    else:
        next_album = None

    tags = Album.album_tags.filter(album__id=id)

    context = {"pics": pics,
               "album": album,
               "refer_albums": refer_albums,
               'pre_album': pre_album,
               'next_album': next_album,
               'tags': tags,
               }
    return render(request, 'mtu/album_info.html', context)


def tagcloud(request):
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    artist_name = request.GET.get('artist_name')
    hometown = request.GET.get('hometown')
    birthday = request.GET.get('birthday')
    career = request.GET.get('career')

    album_tags = request.GET.get('album_tags')
    title = request.GET.get('title')
    institution = request.GET.get('institution')
    artist = request.GET.get('artist')

    # 初始化查询集
    goddesses = Goddess.objects.all()

    # 搜索查询集
    if search:
        # 用 Q对象 进行联合搜索
        goddesses = goddesses.filter(
            Q(artist_name__icontains=search) | Q(hometown__icontains=search)
            | Q(birthday__icontains=search) | Q(body_bra__icontains=search)
        )
    else:
        # 将 search 参数重置为空
        search = ''

    # 艺人查询集
    if artist_name and artist_name != 'None':
        goddesses = goddesses.filter(artist_name=artist_name)

    # 艺人查询集
    if hometown and hometown != 'None':
        goddesses = goddesses.filter(artist_name=artist_name)

    # 摘要查询集
    if birthday and birthday != 'None':
        goddesses = goddesses.filter(birthday=birthday)

    # 标签查询集
    if career and career != 'None':
        goddesses = goddesses.filter(career__in=[career])

    # 初始化查询集
    albums = Album.objects.all()

    # 搜索查询集
    if search:
        # 用 Q对象 进行联合搜索
        albums = albums.filter(
            Q(title__icontains=search) | Q(album_tags__icontains=search)
            | Q(institution__icontains=search) | Q(artist__icontains=search)
        )
    else:
        # 将 search 参数重置为空
        search = ''

    # 专辑艺人查询
    if artist and artist != 'None':
        albums = albums.filter(artist=artist)

    # 专辑查询
    if title and title != 'None':
        albums = albums.filter(title=title)

    # 专辑艺人查询
    if institution and institution != 'None':
        albums = albums.filter(institution=institution)

    # 标签查询集
    if album_tags and album_tags != 'None':
        albums = albums.filter(album_tags__name__in=[album_tags])

    # 初始化查询集
    institutions = Institution.objects.all()

    # 需要传递给模板（templates）的对象
    context = {'goddesses': goddesses, 'albums': albums, 'institutions': institutions, 'search': search,
               }
    # render函数：载入模板，并返回context对象
    return render(request, 'mtu/tag_cloud.html', context)


def alltag(request, pk):
    # 记得在开始部分导入 Tag 类
    tags = Album.album_tags.all()
    t = get_object_or_404(tags, pk=pk)
    albums = Album.objects.filter(album_tags__name__in=[t]).order_by('-created')
    # 每页显示 6 篇文章
    paginator = Paginator(albums, 30)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    albums = paginator.get_page(page)
    return render(request, 'mtu/album_list.html', context={'albums': albums})


def style(request, pk):
    # 记得在开始部分导入 Tag 类
    tags = Album.album_tags.filter(album_tags__name__in=['性感', '诱惑', '气质', '清纯', 'COSPLAY', '御姐',
                                                         '萌系', '极品', '白嫩', '童颜巨乳', '大尺度', '翘臀',
                                                         '美腿', '清新', '女神', '爆乳', '混血', '风骚', '写真',
                                                         '捆绑', '肥臀', '萝莉', '湿身', '美乳', '玉足',
                                                         '私房', '少妇', '尤物', '大奶', '熟女', '妖艳',
                                                         '大胸', '御姐', '甜美', '可爱', '小清新', '养眼',
                                                         '骨感', '童颜', '金发', '长发', '清纯', '纹身', '少女',
                                                         ])
    t = get_object_or_404(tags, pk=pk)
    albums = Album.objects.filter(album_tags__name__in=[t]).order_by('-created')
    # 每页显示 6 篇文章
    paginator = Paginator(albums, 30)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    albums = paginator.get_page(page)
    return render(request, 'mtu/album_list.html', context={'albums': albums})

# def uploads_files(request,):
#
#     if request.method == 'POST':
#         img_form = FileFieldForm(request.POST, request.FILES)
#         files = request.FILES.getlist('file_field')  # 获得多个文件上传进来的文件列表。
#         if img_form.is_valid():  # 表单数据如果合法
#             for f in files:
#                 file = Image(image=f)
#                 file.save()
#             return HttpResponse('成功')
#         return HttpResponse('文件上传失败！')
#
#     else:
#         img_form = FileFieldForm()
#         context = {'img_form': img_form}
#         return render(request, 'mtu/uploadimg.html', context)

# def tag(request, pk):
#     # 记得在开始部分导入 Tag 类
#
#     tags = Album.album_tags.all()
#     t = get_object_or_404(tags, pk=pk)
#     albums = Album.objects.filter(album_tags__name__in=[t]).order_by('-created')
#     # 每页显示 6 篇文章
#     paginator = Paginator(albums, 20)
#     # 获取 url 中的页码
#     page = request.GET.get('page')
#     # 将导航对象相应的页码内容返回给 articles
#     albums = paginator.get_page(page)
#     return render(request, 'mtu/tag_cloud.html', context={'albums':  albums})