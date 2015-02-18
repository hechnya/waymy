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

# @register.inclusion_tag("tags/cart_box.html")
# def cart_box(request):
# 	"""Вставка для виджета отображающего количество разных товаров в корзине"""
# 	cart_items = cart.get_cart_items(request)
#
#     # cart_item_count = cart.cart_distinct_item_count(request)
#     # cart_items = cart.get_cart_items(request)
# 	return {'cart_items': cart_items }

@register.inclusion_tag("tags/category_list.html")
def categories_tree(request):
	"""Возвращает дерево категорий"""
	return {'nodes': Category.objects.filter(is_active=True) }


@register.inclusion_tag("tags/footer.html")
def footer_links():
	"Вставка для виджета отображающего ссылки на статические страницы внизу"
    # products = Product.objects.all()
	flatpage_list = FlatPage.objects.all()
	return {'flatpage_list': flatpage_list }


# The first argument *must* be called "context" here.
def cart_box(context, request):
    cart_i = cart.get_cart_items(request)

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
    return {
        # 'products': products,
        'cart_i': cart_i,
        'device': device,
    }
# Register the custom tag as an inclusion tag with takes_context=True.
register.inclusion_tag('tags/cart_box.html', takes_context=True)(cart_box)


# The first argument *must* be called "context" here.
def lider_box(context, request):
    lider_items = Product.objects.filter(is_bestseller='True')
    return {
        # 'products': products,
        'lider_items': lider_items,
    }
# Register the custom tag as an inclusion tag with takes_context=True.
register.inclusion_tag('tags/lider_box.html', takes_context=True)(lider_box)

# The first argument *must* be called "context" here.
def brand_filter(context, request):
    brand_items = BrandName.objects.all()
    return {
        # 'products': products,
        'brand_items': brand_items,
    }
# Register the custom tag as an inclusion tag with takes_context=True.
register.inclusion_tag('tags/brand_filter.html', takes_context=True)(brand_filter)


# The first argument *must* be called "context" here.
def slider(context, request):
    slides = Slider.objects.all()

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

    return {
        # 'products': products,
        'slides': slides,
        'device': device,
    }
# Register the custom tag as an inclusion tag with takes_context=True.
register.inclusion_tag('tags/slider.html', takes_context=True)(slider)

def menu(context, request):
    pages = Page.objects.all()
    return {
        # 'products': products,
        'pages': pages,
    }
# Register the custom tag as an inclusion tag with takes_context=True.
register.inclusion_tag('tags/menu.html', takes_context=True)(menu)