from django.contrib.sitemaps import Sitemap
from webshop.catalog.models import Product
from webshop.pages.models import Page, Article

class ProductsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Product.objects.all()


class PagesSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Page.objects.all()


class ArticlesSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Article.objects.all()