# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.db import models
from webshop.catalog.models import Product

# Create your models here.
class Slider(models.Model):
    image = models.ImageField(upload_to='slider', verbose_name=u'фото для слайдера')
    text1 = models.CharField(max_length=240, verbose_name=u'Первый текст слайда')
    description = models.TextField(verbose_name=u'Основной текст слайда')
    link = models.CharField(max_length=200, verbose_name=u'Сноска')
    product = models.ForeignKey(Product, verbose_name=u'Выбрать продукт')
    def url(self):
        return '/media/%s' % self.image
    def __unicode__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = (u'Слайды')
        verbose_name = (u'Слайдер на главной странице')
