# -*- coding: utf-8 -*-
# !/usr/bin/env python
from django.db import models
from autoslug import AutoSlugField
from webshop.accounts.models import UserProfile
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


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


class Page(models.Model):
    name = models.CharField(verbose_name=u'Заголовок', max_length=100)
    slug = models.SlugField(verbose_name=u'Ссылка на услугу',
                            max_length=50,
                            unique=True,
                            help_text=u'Ссылка формируется автоматически при заполнении.')
    text = RichTextField(verbose_name=u'Текст страницы', config_name='default')
    is_main = models.BooleanField(verbose_name=u'На главную')

    old_id = models.CharField(max_length=20, verbose_name=u'id страницы со старого сайта для редиректа', blank=True)
    #meta = models.OneToOneField(MetaInPages, blank=True, null=True)

    meta_title = models.CharField(verbose_name=u'мета title', max_length=100, blank=True)
    meta_description = models.CharField(verbose_name=u'мета description', max_length=240, blank=True)
    class Meta:
        verbose_name_plural = u'Страницы'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/page/%s' % self.slug


class Article(models.Model):
    name = models.CharField(verbose_name=u'Заголовок', max_length=100)
    image = models.ImageField(verbose_name=u'Изображение', upload_to='articles')
    slug = models.SlugField(verbose_name=u'Ссылка на услугу',
                            max_length=50,
                            unique=True,
                            help_text=u'Ссылка формируется автоматически при заполнении.')
    text = RichTextField(verbose_name=u'Текст страницы', config_name='default')
    old_id = models.CharField(max_length=20, verbose_name=u'id страницы со старого сайта для редиректа', blank=True)
    
    #мета описание для статьи
    meta_title = models.CharField(verbose_name=u'мета title', max_length=100, blank=True)
    meta_description = models.CharField(verbose_name=u'мета description', max_length=240, blank=True)
    #meta = models.OneToOneField(MetaInPages, blank=True, null=True)

    class Meta:
        verbose_name_plural = u'Статьи'

    def __unicode__(self):
        return self.name

    def url(self):
        return '/articles/%s' % self.slug

    def get_absolute_url(self):
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

