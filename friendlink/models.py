from django.db import models
# timezone 用于处理时间相关事务。
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
import os


class Link_type(models.Model):
    """
    栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = '收藏网址类别'
        verbose_name_plural = "收藏网址类别"
        # 为了在后台显示中文

    def __str__(self):
        return self.title


def link_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.title, ext)
    # return the whole path to the file
    return os.path.join("friendlink",  filename)


class Friend_link(models.Model):
    title = models.CharField('标题', max_length=100)
    abstract = models.TextField('摘要', max_length=200, blank=True)
    url = models.URLField('网址')
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    logo = ProcessedImageField(upload_to=link_logo_path, processors=[ResizeToFit(width="128", height="128")],
                               format='png',
                               options={'quality': 100}, blank=True)

    # 文章栏目的 “一对多” 外键
    link_type = models.ForeignKey(
        Link_type,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='friend_link'
    )

    class Meta:
        verbose_name = '收藏的网址'
        verbose_name_plural = "收藏的网址"
        # 为了在后台显示中文

    def __str__(self):
        return self.title