# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url


urlpatterns = patterns('webshop.pages.views',
    # url(r'^(?P<slug>[-_\w]+)/$', PageView.as_view(), name='page'),
    # url(r'^', PageList.as_view(), name='blog_posts'),
    url(r'^page/(?P<slug>[-_\w]+)/$', 'pageView',
        {'template_name':'pages/page.html'},
        name='page'),

    url(r'^articles/$', 'articlesView',
        {'template_name':'pages/articles.html'},
        name='articles'),

    url(r'^articles/(?P<slug>[-_\w]+)/$', 'articleView',
        {'template_name':'pages/article.html'},
        name='article'),

    url(r'^404/$', 'view_404',
        {'template_name':'404.html'},
        name='view_404'),
)
