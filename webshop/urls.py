# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, include, url
from django.contrib import admin
from webshop import settings
from django.conf.urls import handler404 
from webshop import views

admin.autodiscover()

from webshop.catalog.sitemap import ProductsSitemap, PagesSitemap, ArticlesSitemap, CategorySitemap, StaticViewSitemap
sitemaps = {
    'products': ProductsSitemap,
    'pages': PagesSitemap,
    'articles': ArticlesSitemap,
    'main': StaticViewSitemap,
    'category': CategorySitemap
}

urlpatterns = patterns(
    '',
    url(r'^admin_tools/', include('admin_tools.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    # General application URLs
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('webshop.accounts.urls')),
    url(r'^', include('webshop.catalog.urls')),
    url(r'^', include('webshop.pages.urls')),
    url(r'^cart/', include('webshop.cart.urls')),
    url(r'^checkout/', include('webshop.checkout.urls')),
    url(r'^', include('webshop.news.urls')),
    url(r'^search/', include('webshop.search.urls')),
    url(r'^review/$', include('webshop.pages.reviewurls')),
    # редиректы со старого сайта
    url(r'^index.php/', include('webshop.pages.urls_redirect')),

    # enable language choice
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^set_language/$', 'django.views.i18n.set_language',
        name='set_language'),

    url(r'^robokassa/', include('robokassa.urls')),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    # (r'^robots\.txt$', include('robots.urls')),
    (r'^robots.txt$','webshop.catalog.views.robots'),
)

urlpatterns += patterns(
    '',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)


# handler404 = 'webshop.views.file_not_found_404'
handler404 = views.error404
