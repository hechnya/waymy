# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url


urlpatterns = patterns('webshop.pages.views',

    url('^\w*', 'redirectView',
         {'template_name': 'pages/test.html'}),
    # ?route=information/news.news_id=
)