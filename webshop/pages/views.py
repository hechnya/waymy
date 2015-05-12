# -*- coding: utf-8 -*-
# !/usr/bin/env python
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from webshop.pages.forms import *
from models import MetaInPages
from webshop.catalog.models import Product


# def get_meta(func):
#     def tmp(request, *args, **kwargs):
#         try:
#             meta_object = MetaInPages.objects.get(link=request.path)
#         except:
#             pass
#         return func(request, *args, **kwargs)
#     return tmp
#
#
# @get_meta
def pageView(request, slug, template_name="pages/page.html", *args):
    page = Page.objects.get(slug=slug)
    try:
        meta_object = MetaInPages.objects.get(link=request.path)
    except:
        pass
    request.breadcrumbs('%s' % page.name, request.path_info)
    if request.user.is_superuser:
        try:
            if request.method == 'POST':
                postdata = request.POST.copy()
                form = PageForm(postdata)
                if form.is_valid():
                    page.name = postdata.get('name', '')
                    page.slug = postdata.get('slug', '')
                    page.text = postdata.get('text', '')
                    page.is_main = False
                    page.save()
                    # new_review = form.save(commit=False)
                    form = PageForm(instance=page)
                    url = urlresolvers.reverse(request.path_info)
                    return HttpResponseRedirect(url)
            else:
                # user_profile = request.user
                if request.user.is_superuser:
                    form = PageForm(instance=page)
        except:
            text = u'Вы не имеете право'
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def articlesView(request, template_name="pages/articles.html"):
    # :TODO не плохое решение метотэгов на основе текущего урла
    try:
        meta_object = MetaInPages.objects.get(link=request.path)
    except:
        pass
    articles = Article.objects.all()
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def articleView(request, slug, template_name="pages/article.html"):
    #try:
        #meta_object = MetaInPages.objects.get(link=request.path)
    #except:
        #pass
    article = Article.objects.get(slug=slug)
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def review_form_view(request, template_name="pages/review.html"):
    try:
        meta_object = MetaInPages.objects.get(link=request.path)
    except:
        pass
    request.breadcrumbs(u'Отзывы', request.path_info)
    try:
        current_userProfile = UserProfile.objects.get(user=request.user)
        reviews = Review.objects.all()
        if request.method == 'POST':
            postdata = request.POST.copy()
            form = ReviewForm(postdata)
            if form.is_valid():
                new_review = Review()
                new_review.review = postdata.get('review', '')
                new_review.user = request.user
                new_review.save()
                url = urlresolvers.reverse('my_account')
                return HttpResponseRedirect(url)
        else:
            user_profile = request.user
            form = ReviewForm(instance=user_profile)
    except:
        text = u'Вы не заполнили свой профиль'
    reviews = Review.objects.all()
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def redirectView(request, template_name="404.html"):

    # если кто-то хочет зайти на статью по старому url
    if request.GET.get('route') == 'information/news':
        news_id = request.GET.get('news_id')
        articles = Article.objects.all()
        for article in articles:
            if article.old_id == news_id:
                return redirect('/articles/%s/' % article.slug, permanent=True)
    
    # если кто-то хочет зайти на страницу по старому url
    elif request.GET.get('route') == 'information/information':
        information_id = request.GET.get('information_id')
        pages = Page.objects.all()
        for page in pages:
            if page.old_id == information_id:
                return redirect('/page/%s' % page.slug, permanent=True)
     
    # если кто-то хочет зайти на товар по старому url
    elif request.GET.get('route') == 'product/product':
        product_id = request.GET.get('product_id')
        products = Product.objects.all()
        for product in products:
            ids = product.old_id.split(',')
            for id_item in ids:
                if id_item == product_id:
                    return redirect('/product/%s' % product.slug, permanent=True)
    
    return redirect('/404')
    #return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def view_404(request, template_name="404.html"):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
     
