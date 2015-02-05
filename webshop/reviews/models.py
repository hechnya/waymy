# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.db import models
from webshop.accounts.models import UserProfile
from webshop.catalog.models import Product
from ckeditor.fields import RichTextField

class ReviewsProduct(models.Model):
    userProfile = models.ForeignKey(UserProfile, verbose_name=u'Пользователь', help_text=u'Выберите пользователя к которому относится данный отзыв')
    product = models.ForeignKey(Product, verbose_name=u'Продукт', help_text=u'Выберите продукт к которому относиться данный отзыв')
    text = RichTextField()
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.userProfile.shipping_name



