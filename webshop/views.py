# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template


def error404(request):
    """Представление для страницы которая не найдена"""
    page_title = _(u'Page Not Found')

    response = render_to_response('404.html', locals(), context_instance=RequestContext(request))
    response.status_code = 404
    return response

# def error404(request):
#
#     # 1. Load models for this view
#     #from idgsupply.models import My404Method
#
#     # 2. Generate Content for this view
#     template = get_template('404.htm')
#     context = Context({
#         'message': 'All: %s' % request,
#         })
#
#     # 3. Return Template for this view + Data
#     return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404)
