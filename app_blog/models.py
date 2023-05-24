from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# 网站信息
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.html import format_html


class Site(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='网站标题')
    abstract = models.CharField(max_length=128, verbose_name='网站简介')
    key_words = models.CharField(max_length=128, verbose_name='网站关键字')
    record = models.CharField(max_length=32, verbose_name='网站备案号')
    create_date = models.DateTimeField(verbose_name='建站日期')
    version = models.CharField(max_length=10, verbose_name='网站版本号')
    icon = models.FileField(verbose_name='网站图标', upload_to='site_icon/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '网站信息'


# 个人信息
class MyInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='名字')
    job = models.CharField(max_length=128, verbose_name='工作')
    email = models.EmailField(max_length=64, verbose_name='邮箱')
    site_url = models.CharField(max_length=32, verbose_name='网站链接')
    addr = models.CharField(max_length=16,verbose_name='地址')
    bilibili_url = models.URLField(verbose_name='哔哩哔哩链接')
    github_url = models.URLField(verbose_name='Github链接')
    wechat_img = models.FileField(verbose_name='微信图片', upload_to='my_info/')
    qq_img = models.FileField(verbose_name='QQ图片', upload_to='my_info/')

    class Meta:
        verbose_name_plural = '个人信息'


# 用户表
class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    sign_choice = (
        (0, '用户名注册'),
        (1, '手机号注册'),
        (2, '邮箱注册'),
        (3, 'QQ注册'),
    )
    nick_name = models.CharField(max_length=16, verbose_name='昵称')
    sign_status = models.IntegerField(default=0, choices=sign_choice, verbose_name='注册方式')
    tel = models.CharField(max_length=12, verbose_name='手机号', null=True, blank=True)
    integral = models.IntegerField(default=20, verbose_name='用户积分')
    token = models.CharField(max_length=64, verbose_name='TOKEN', null=True, blank=True)
    avatar = models.ForeignKey(
        to='Avatars',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='用户头像',
        null=True
    )
    collects = models.ManyToManyField(
        to='Article',
        verbose_name='收藏的文章',
        blank=True
    )

    class Meta:
        verbose_name_plural = '用户'


# 用户头像表
class Avatars(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='用户头像地址', upload_to='avatars/')

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = '用户头像'


# sender=你要删除或修改文件字段所在的类
@receiver(pre_delete, sender=Avatars)
def download_delete(instance, **kwargs):
    # file是保存文件或图片的字段名
    instance.url.delete(False)


# 文章表
class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='标题', null=True, blank=True)
    abstract = models.CharField(max_length=128, verbose_name='文章简介', null=True, blank=True)
    content = models.TextField(verbose_name='文章内容', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name='文章发布日期', auto_now_add=True, null=True)
    change_date = models.DateTimeField(verbose_name='文章修改日期', auto_now=True, null=True)
    status_choice = (
        (0, '未发布'),
        (1, '已发布'),
    )
    status = models.IntegerField(verbose_name='文章保存', choices=status_choice)
    recommend = models.BooleanField(verbose_name='是否上推荐', default=True)
    cover = models.ForeignKey(
        to='Cover',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='文章封面', null=True, blank=True
    )
    look_count = models.IntegerField(verbose_name='文章阅读量', default=0)
    comment_count = models.IntegerField(verbose_name='文章评论量', default=0)
    digg_count = models.IntegerField(verbose_name='文章点赞量', default=0)
    collects_count = models.IntegerField(verbose_name='文章收藏数', default=0)
    category_choice = (
        (0, '前端'),
        (1, '后端'),
    )
    category = models.IntegerField(verbose_name='文章分类', choices=category_choice, null=True, blank=True)
    tag = models.ManyToManyField(
        to='Tags',
        verbose_name='文章标签',
        blank=True
    )
    author = models.CharField(max_length=16, verbose_name='作者', null=True, blank=True)
    source = models.CharField(max_length=32, verbose_name='来源', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章'


# 评论表
class Comment(models.Model):
    nid = models.AutoField(primary_key=True)
    digg_count = models.IntegerField(verbose_name='点赞', default=0)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid', on_delete=models.CASCADE, null=True)
    content = models.TextField(verbose_name='评论内容')
    comment_count = models.IntegerField(verbose_name='子评论数', default=0)
    drawing = models.TextField(verbose_name='配图', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    parent_comment = models.ForeignKey('self', verbose_name='是否是父评论', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '评论'


# 新闻的爬取记录
class New(models.Model):
    nid = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(verbose_name='获取时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = '新闻爬取'


# 文章封面
class Cover(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='文章封面地址', upload_to='article_img/')

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = '文章封面'


@receiver(pre_delete, sender=Cover)
def cover_delete(instance, **kwargs):
    instance.url.delete(False)


# 标签表
class Tags(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=16, verbose_name='标签名字')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章标签'


# 回忆录
class History(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='事件名称')
    content = models.TextField(verbose_name='事件内容')
    create_date = models.DateTimeField(verbose_name='创建时间', null=True)
    drawing = models.TextField(verbose_name='配图组·以;隔开', null=True, blank=True)

    class Meta:
        verbose_name_plural = '回忆录'


# 心情
class Moods(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, verbose_name='发布人')
    create_date = models.DateTimeField(verbose_name='发布时间', auto_now=True)
    content = models.TextField(verbose_name='心情内容')
    drawing = models.TextField(verbose_name='配图组·以;隔开', null=True, blank=True)
    comment_count = models.IntegerField(verbose_name='评论数', default=0)
    digg_count = models.IntegerField(verbose_name='点赞数', default=0)
    avatar = models.ForeignKey(
        to='Avatars',
        to_field='nid',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='心情的发布头像'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '心情'


# 心情评论
class MoodComment(models.Model):
    nid = models.AutoField(primary_key=True)
    avatar = models.ForeignKey(
        to='Avatars',
        to_field='nid',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='心情的发布头像'
    )
    name = models.CharField(max_length=16, verbose_name='评论人', null=True)
    content = models.TextField(verbose_name='评论内容')
    digg_count = models.IntegerField(verbose_name='点赞数', default=0)
    mood = models.ForeignKey(
        to='Moods',
        to_field='nid',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='评论的心情'
    )
    create_date = models.DateTimeField(verbose_name='评论时间', auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '心情评论'


# 网站导航
class Navs(models.Model):
    nid = models.AutoField(primary_key=True)
    nav_category = models.ForeignKey(
        to='NavCategory',
        to_field='nid',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='网站导航的分类'
    )
    icon_href = models.URLField(verbose_name='图标链接', help_text='在线链接', null=True, blank=True)
    icon = models.FileField(
        verbose_name='网站图标',
        null=True,
        blank=True,
        upload_to='site_icon/',
        help_text='文件优先级大于在线链接'
    )
    title = models.CharField(max_length=32, verbose_name='网站标题')
    abstract = models.CharField(max_length=128, verbose_name='网站简介', null=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    href = models.URLField(verbose_name='网站链接')
    status_choice = (
        (0, '待审核'),
        (1, '已通过'),
        (2, '被驳回'),
    )
    status = models.IntegerField(verbose_name='导航状态', choices=status_choice, default=0)

    def color_state(self):
        if self.status == 0:
            assign_state_name = '待审核'
            color_code = '#ec921e'
        elif self.status == 1:
            assign_state_name = '已通过'
            color_code = 'green'
        else:
            assign_state_name = '被驳回'
            color_code = 'red'
        return format_html(
            '<scan style="color:{};">{}</scan>',
            color_code,
            assign_state_name,
        )

    color_state.short_description = '导航状态'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '网站导航'


# 导航分类
class NavCategory(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=16, verbose_name='分类标题')
    icon = models.CharField(max_length=32, verbose_name='分类图标')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '导航分类'


# 站点背景
class Menu(models.Model):
    nid = models.AutoField(primary_key=True)
    menu_title = models.CharField(max_length=16, verbose_name='菜单名称', null=True)
    menu_title_en = models.CharField(max_length=32, verbose_name='菜单英文名称', null=True)
    title = models.CharField(max_length=32, verbose_name='slogan', null=True)
    abstract = models.TextField()
    abstract_time = models.IntegerField()
    rotation = models.BooleanField()
    menu_url = models.ForeignKey(
        to='MenuImg',
        verbose_name='菜单图片',
        help_text='可以多选,多选就会轮播',
        on_delete=models.CASCADE
    )
    menu_rotation = models.BooleanField(verbose_name='是否轮播banner图', help_text='多选默认会轮播', default=False)
    menu_time = models.IntegerField(verbose_name='背景图切换时间', help_text='单位秒,默认是8秒', default=8)

    class Meta:
        verbose_name_plural = '站点背景'


# 站点背景图
class MenuImg(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='图片地址', upload_to='site_bg/')

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = '站点背景图'


# 广告表
class Advert(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='产品名称', null=True)
    href = models.URLField(verbose_name='跳转链接')
    img = models.FileField(verbose_name='图片地址', null=True, blank=True, help_text='单图', upload_to='advert/')
    img_list = models.TextField(verbose_name='图片组', null=True, blank=True, help_text='上传图片请用线上地址,使用;隔开多张图片')
    is_show = models.BooleanField(verbose_name='是否展示', default=False)
    author = models.CharField(max_length=32, verbose_name='广告主', null=True, blank=True)
    abstract = models.CharField(max_length=128, verbose_name='产品简介', null=True, blank=True)

    class Meta:
        verbose_name_plural = '广告'


# 反馈信息
class Feedback(models.Model):
    nid = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='邮箱')
    content = models.TextField(verbose_name='反馈信息')
    status = models.BooleanField(verbose_name='是否处理', default=False)
    processing_content = models.TextField(verbose_name='回复的内容', null=True, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '用户反馈'
