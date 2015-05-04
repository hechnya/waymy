# -*- coding: utf-8 -*-
# !/usr/bin/env python
from django.db import models
from autoslug import AutoSlugField
from webshop.accounts.models import UserProfile
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Page(models.Model):
    name = models.CharField(verbose_name=u'Заголовок', max_length=100)
    slug = AutoSlugField(default='default', editable=True)
    text = RichTextField(verbose_name=u'Текст страницы', config_name='default')
    is_main = models.BooleanField(verbose_name=u'На главную')

    class Meta:
        verbose_name_plural = u'Страницы'

    def __unicode__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(verbose_name=u'Заголовок', max_length=100)
    image = models.ImageField(
        verbose_name=u'Изображение',
        upload_to='articles')
    slug = AutoSlugField(default='default', editable=True)
    text = RichTextField(verbose_name=u'Текст страницы', config_name='default')
    old_id = models.CharField(max_length=20, verbose_name=u'id страницы со старого сайта для редиректа', blank=True)

    class Meta:
        verbose_name_plural = u'Статьи'

    def __unicode__(self):
        return self.name

    def url(self):
        return '/articles/%s' % self.slug


class Review(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    review = models.TextField(verbose_name=u'Отзыв')

    def __unicode__(self):
        userName = UserProfile.objects.get(user=self.user)
        if userName.shipping_name:
            return u'Отзыв: ' + userName.shipping_name
        else:
            return u'Отзыв: ' + self.user.username

    class Meta:
        verbose_name_plural = (u'Отзывы пользователей')


class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Имя ссылки')


class MetaInPages(models.Model):
    title = models.CharField(
        u'Title', max_length=255,
        help_text=u'Содержимое для title страницы',
        blank=True)
    description = models.CharField(
        u'Мета description',
        max_length=255,
        help_text=u'Содержимое для мета тега description',
        blank=True)
    link = models.CharField(
        u'Ссылка на страницу', max_length=255,
        help_text=u'Указывать необходимо путь относительно домена,'
        u' например "/page/kontakty/", '
        u'косая черта обязательна как в начале так и в конце url', blank=True)

    class Meta:
        verbose_name_plural = u'Настройка мета данных для страниц'
        verbose_name = u'Мета данные'

    def __unicode__(self):
        return u'Мета %s' % self.title
