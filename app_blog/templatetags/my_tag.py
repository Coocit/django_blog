from django import template

# 注册
register = template.Library()


# 自定义过滤器
# @register.filter
# def add1(item):
#     return int(item) + 1


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name):
    print(menu_name)
    img_list = [
        "/static/img/slideshow1.jpg",
        "/static/img/slideshow2.jpg",
        "/static/img/slideshow3.jpg"
    ]
    return {"img_list": img_list}
