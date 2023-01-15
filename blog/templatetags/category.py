# 这里自定义标签

from blog.models import Category, Sidebar, Post
from django import template


register = template.Library()   # 向模版标签中进行注册


@register.simple_tag
def get_category_list():
    return Category.objects.all()


@register.simple_tag
def get_sidebar_list():
    # 侧边栏
    return Sidebar.get_sidebar()


@register.simple_tag
def get_new_post():
    # 最新文章
    return Post.objects.order_by('-pub_date')[:8]


@register.simple_tag
def get_hot_post():
    # 手动热门推荐
    return Post.objects.filter(is_hot=True)[:8]


@register.simple_tag
def get_hot_pv_post():
    # 手动热门推荐
    return Post.objects.order_by('-pv')[:8]


@register.simple_tag
def get_archives():
    # 文章归档，按照年，月进行归档
    return Post.objects.dates('add_date', 'month', order='DESC')[:8]
