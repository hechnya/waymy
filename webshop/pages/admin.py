# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin
from webshop.pages.models import Page, Article, Review, MetaInPages

# class MetaInlineAdmin(admin.StackedInline):
#     """Добавление изображений продукта"""
#     model = MetaInPages
#     extra = 0


class PageAdmin(admin.ModelAdmin):
    model = Page
    prepopulated_fields = {'slug':('name',)}


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Page, PageAdmin)
admin.site.register(Review)
admin.site.register(Article, ArticleAdmin)
admin.site.register(MetaInPages)