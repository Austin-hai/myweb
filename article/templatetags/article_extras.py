from django import template

from ..models import ArticlePost, ArticleColumn
from django.db.models.aggregates import Count


register = template.Library()


@register.inclusion_tag('article/_archives.html', takes_context=True)
def show_archives(context):
    date_list = ArticlePost.objects.dates('created', 'month', order='DESC')
    return {
        'date_list': date_list,
    }


@register.inclusion_tag('article/_categories.html', takes_context=True)
def show_categories(context):
    # columns = ArticleColumn.objects.all()
    columns = ArticleColumn.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)
    return {
        'category_list': columns,
    }


@register.inclusion_tag('article/_tags.html', takes_context=True)
def show_tags(context):
    tags = ArticlePost.article_tags.all()
    return {
        'tag_list': tags,
    }