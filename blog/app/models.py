# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    location = models.CharField(_('address'), max_length=30, blank=True)
    birth_date = models.DateField(_('birthday'), null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'part'),
        ('p', 'Published'),
    )   # 文章的状态

    author = models.ForeignKey('auth.User',
                               verbose_name=_('author'),
                               on_delete=models.CASCADE,
                               )
    title = models.CharField(_('title'), max_length=100)
    body = models.TextField(_('body'))

    # auto_now_add : 创建时间戳，不会被覆盖
    created_time = models.DateTimeField(_('create time'), auto_now_add=True)

    # auto_now: 自动将当前时间覆盖之前时间
    last_modified_time = models.DateTimeField(_('last modified time'),
                                              auto_now=True)

    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES)
    abstract = models.CharField(_('abstract'),
                                max_length=54,
                                blank=True,
                                null=True,
                                help_text=_('Optional, if it is a space, '
                                            'the first 54 characters are '
                                            'taken from the body.'))
    # 阅读量
    views = models.PositiveIntegerField(_('view times'), default=0)
    # 点赞数
    likes = models.PositiveIntegerField(_('great times'), default=0)
    # 是否置顶
    topped = models.BooleanField(_('placed at the top'), default=False)
    # 目录分类
    # on_delete 当指向的表被删除时，将该项设为空
    category = models.ForeignKey('Category', verbose_name=_('category'),
                                 null=True,
                                 on_delete=models.SET_NULL)
    # 标签云
    tags = models.ManyToManyField('Tag', verbose_name=_('tags'), blank=True)

    def __str__(self):
        return self.title

    class Meta:
        # Meta 包含一系列选项，这里的ordering表示排序, - 表示逆序
        # 即当从数据库中取出文章时，以文章最后修改时间逆向排序
        ordering = ['-last_modified_time']

    def get_absolute_url(self):
        return reverse('app:detail', kwargs={'article_id': self.pk})


class Category(models.Model):
    """
    另外一个表,储存文章的分类信息
    文章表的外键指向
    """
    name = models.CharField(_('category name'), max_length=20)
    created_time = models.DateTimeField(_('create time'), auto_now_add=True)
    last_modified_time = models.DateTimeField(_('last modified time'),
                                              auto_now=True)

    def __str__(self):
        return self.name


class BlogComment(models.Model):
    user = models.ForeignKey('auth.User',
                             verbose_name=_('reviewers'),
                             on_delete=models.CASCADE)
    body = models.TextField(_('comment content'))
    created_time = models.DateTimeField(_('create time'), auto_now_add=True)
    parent_comment = models.ForeignKey('BlogComment',
                                       verbose_name=_('parent comment'),
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       null=True
                                       )
    article = models.ForeignKey('Article', verbose_name=_('article belongs'),
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.body[:20]


class Tag(models.Model):
    """
    tag(标签云)对应的数据库
    """
    name = models.CharField(_('tag name'), max_length=20)
    created_time = models.DateTimeField(_('create time'), auto_now_add=True)
    last_modified_time = models.DateTimeField(_('last modified time'),
                                              auto_now=True)

    def __str__(self):
        return self.name


class Suggest(models.Model):
    """
    意见存储
    """
    user = models.ForeignKey('auth.User',
                             verbose_name=_('suggester'),
                             on_delete=models.CASCADE)
    suggest = models.TextField(_('opinion'), max_length=200)
    suggest_time = models.DateTimeField(_('creation time'), auto_now_add=True)

    def __str__(self):
        return self.suggest