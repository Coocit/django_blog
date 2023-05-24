"""
URL configuration for django_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from app_blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('news/', views.news),   # 新闻
    # path('moods/', moods.moods),    # 心情
    # path('sites/', sites.sites),    # 站点导航
    #
    # path('get_code_img/', login.get_code_img),  # 验证码
    #
    # path('login/', login.Login.as_view()),     # 登录
    # path('sign/', login.Sign.as_view()),     # 注册
    # path('logout/', login.logout),     # 注销
    #
    # path('backend/', back_admin.backend),   # 个人中心
    # path('edit_avatar/', back_admin.Avatars.as_view()),     # 修改头像
    # path('reset_password/', back_admin.Password.as_view()),  # 重置密码
    # path('add_article/', back_admin.AddArticle.as_view()),  # 添加文章
    # re_path(r'edit_article/(?P<nid>\d+)', back_admin.EditArticle.as_view()),    # 编辑文章
    # re_path(r'article/(?P<nid>\d+)', article.Article.as_view())     # 文章详情

    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
