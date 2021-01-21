from django import template

from ..models import Goddess, Album, Image
from django.db.models.aggregates import Count

register = template.Library()


@register.inclusion_tag('mtu/mtu_tags.html', takes_context=True)
def show_locations(context):
    locations = Goddess.objects.filter(hometown__in=['大陆', '日本', '欧美', '港台', '韩国', '乌克兰'])
    return {
        'locations': locations,
    }


@register.inclusion_tag('mtu/mtu_tags.html', takes_context=True)
def show_careers(context):
    careers = Goddess.objects.filter(career__in=['学生妹', '女优', '秘书', '嫩模', '护士', '空姐',
                                                 'ShowGirl', '足球宝贝', '车模', '模特', '主播', '演员',
                                                 ])
    return {
        'careers': careers,
    }


@register.inclusion_tag('mtu/mtu_tags.html', takes_context=True)
def show_styles(context):
    # tags = Album.album_tags.all()
    styles = Album.objects.filter(album_tags__name__in=['性感', '诱惑', '气质', '清纯', 'COSPLAY', '御姐',
                                                        '萌系', '极品', '白嫩', '童颜巨乳', '大尺度', '翘臀',
                                                        '美腿', '清新', '女神', '爆乳', '混血', '风骚', '写真',
                                                        '捆绑', '肥臀', '萝莉', '湿身', '美乳', '玉足',
                                                        '私房', '少妇', '尤物', '大奶', '熟女', '妖艳',
                                                        '大胸', '御姐', '甜美', '可爱', '小清新', '养眼',
                                                        '骨感', '童颜', '金发', '长发', '清纯', '纹身', '少女',
                                                        ])

    return {
        'styles': styles,
    }


@register.inclusion_tag('mtu/mtu_tags.html', takes_context=True)
def show_scenes(context):
    scenes = Album.objects.filter(album_tags__name__in=['街拍', '浴室', '户外', '沙滩', '泳池', '私房照',
                                                        '床上', '室内', '阳台', '校园', '演唱会',
                                                        ])
    return {
        'scenes': scenes,
    }


@register.inclusion_tag('mtu/mtu_tags.html', takes_context=True)
def show_cloths(context):
    cloths = Album.objects.filter(album_tags__name__in=['透视装', '情趣内衣', '丝袜', '丁字裤', '情趣睡衣', '内衣',
                                                        '裤袜', '蕾丝', '制服', '黑丝', 'OL制服', '旗袍',
                                                        '超短裙', '女仆', '超短裙', '网袜', '泳装', '比基尼',
                                                        '高跟鞋', '兔女郎', '紧身衣', '肚兜', 'jk制服', '吊带',
                                                        '低胸装', '短裤', '猫女郎', '水手服', '长靴', '和服',
                                                        '护士装',
                                                        ])
    return {
        'cloths': cloths,
    }


@register.inclusion_tag('mtu/mtu_tags.html', takes_context=True)
def show_tags(context):
    tags = Album.album_tags.all()
    return {
        'tag_list': tags,
    }
