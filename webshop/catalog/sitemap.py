from django.contrib.sitemaps import Sitemap
from webshop.catalog.models import Product, Category
from webshop.pages.models import Page, Article
from django.contrib import sitemaps
from django.core.urlresolvers import reverse

class ProductsSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Product.objects.all()


class PagesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Page.objects.all()


class ArticlesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Article.objects.all()


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Category.objects.all()


# class StaticViewSitemap(sitemaps.Sitemap):
#     priority = 1
#     changefreq = 'monthly'

#     def items(self):
#         return ['main',]

#     def location(self, item):
#         return reverse(item)