# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import template
from django.contrib.flatpages.models import FlatPage
from django.template import context

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from webshop.cart import cart
from webshop.catalog.models import Category, Product, ProductImage, BrandName
from webshop.slider.models import Slider
from webshop.checkout import checkout
from webshop.catalog.models import Category
from webshop.pages.models import Page
from webshop.catalog import mobile

register = template.Library()


def categories_tree(context, request):
    return {
        'nodes': Category.objects.filter(is_active=True),

    }
register.inclusion_tag('tags/category_list.html', takes_context=True)(categories_tree)


def categories_tree_mobile(context, request):
    return {
        'nodes': Category.objects.filter(is_active=True),

    }
register.inclusion_tag('tags/category_list_mobile.html', takes_context=True)(categories_tree_mobile)


@register.inclusion_tag("tags/footer.html")
def footer_links(request):
    flatpage_list = FlatPage.objects.all()
    return {
        'flatpage_list': flatpage_list,
    }

def cart_box(context, request):
    cart_i = cart.get_cart_items(request)
    quantity = cart.cart_distinct_item_count(request)
    device = checkDevice(request)
    return {
        'cart_i': cart_i,
        'device': device,
        'quantity': quantity
    }
register.inclusion_tag('tags/cart_box.html', takes_context=True)(cart_box)

def lider_box(context, request):
    lider_items = Product.objects.filter(is_bestseller='True')
    return {
        'lider_items': lider_items,
    }
register.inclusion_tag('tags/lider_box.html', takes_context=True)(lider_box)

def brand_filter(context, request):
    brand_items = BrandName.objects.all()
    return {
        'brand_items': brand_items,
    }
register.inclusion_tag('tags/brand_filter.html', takes_context=True)(brand_filter)

def slider(context, request):
    slides = Slider.objects.all()
    device = checkDevice(request)
    return {
        'slides': slides,
        'device': device,
    }
register.inclusion_tag('tags/slider.html', takes_context=True)(slider)

def menu(context, request):
    pages = Page.objects.all()
    return {
        'pages': pages,
    }

register.inclusion_tag('tags/menu.html', takes_context=True)(menu)


def checkDevice(request):
    # определение устройства
    user_agent = request.META.get("HTTP_USER_AGENT")
    http_accept = request.META.get("HTTP_ACCEPT")
    device = ''
    if user_agent and http_accept:
        agent = mobile.UAgentInfo(userAgent=user_agent, httpAccept=http_accept)
        if agent.detectTierIphone():
            device = 'mobile'
        if agent.detectMobileQuick():
            device = 'mobile'
        if agent.detectTierTablet():
            device = 'tablet'

    return device