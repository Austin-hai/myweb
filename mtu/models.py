# timezone 用于处理时间相关事务。
from django.utils import timezone
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
import uuid
import os
# Django-taggit
from taggit.managers import TaggableManager


def Institution_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.institution_name, ext)
    # return the whole path to the file
    return os.path.join("Institution", filename)


class Institution(models.Model):
    # 机构信息
    institution_name = models.CharField(max_length=100)

    thumb = ProcessedImageField(upload_to=Institution_directory_path,
                                processors=[ResizeToFit(width="150", height="150")],
                                format='JPEG',
                                options={'quality': 100}, blank=True)

    # 机构描述。保存大量文本使用 TextField
    description = models.TextField(blank=True)

    # 机构特色
    style = models.CharField(max_length=100, blank=True)

    # 机构成立时间
    created = models.DateField(blank=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.institution_name


def Goddess_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.artist_name, ext)
    # return the whole path to the file
    return os.path.join("goddess", instance.artist_name, filename)


# 女神数据集
class Goddess(models.Model):
    # 女神信息
    artist_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100, blank=True)
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    ranking = models.PositiveIntegerField(default=0, blank=True)
    hotpoint = models.PositiveIntegerField(default=0, blank=True)
    hometown = models.CharField(max_length=100, blank=True)
    career = models.CharField(max_length=100, default='模特')
    thumb = ProcessedImageField(upload_to=Goddess_directory_path, processors=[ResizeToFit(width="158", height="216")],
                                format='JPEG',
                                options={'quality': 100}, blank=True)
    birthday = models.DateField(auto_now=False, blank=True)
    age = models.IntegerField(default=30, blank=True)
    body_height = models.PositiveIntegerField(default=165, blank=True)
    body_weight = models.PositiveIntegerField(default=40, blank=True)
    body_bra = models.CharField(max_length=100, default=88, blank=True)
    body_waist = models.PositiveIntegerField(default=60, blank=True)
    body_butt = models.PositiveIntegerField(default=88, blank=True)
    # 文章正文。保存大量文本使用 TextField
    description = models.TextField(blank=True)

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('ranking',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.artist_name


def Album_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.title, ext)
    # return the whole path to the file
    return os.path.join("albums", instance.title, filename)


# 博客文章数据模型
class Album(models.Model):
    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 专辑的艺人
    # 艺人 专辑的 “一对多” 外键
    artist = models.ForeignKey(Goddess,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               related_name='artist')

    institution = models.ForeignKey(Institution,
                                    null=True,
                                    blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='album')

    thumb = ProcessedImageField(upload_to=Album_directory_path, processors=[ResizeToFit(width=224, height=322)],
                                format='JPEG',
                                options={'quality': 90}, blank=True)

    # 文章标签
    album_tags = TaggableManager(blank=True)

    description = models.TextField(blank=True)

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title


def AlbumImage_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    return os.path.join("albums", instance.album_title, filename)


class Image(models.Model):
    album_title = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.PROTECT)

    image = ProcessedImageField(upload_to=AlbumImage_directory_path, processors=[ResizeToFit(1200)], format='JPEG',
                                options={'quality': 90})
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.album_title
