# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.utils import simplejson
from webshop.cart import cart
from webshop.catalog.forms import ProductAddToCartForm
from webshop.cart.delivery import calculate_delivery_price
from webshop.catalog.models import *
# from webshop.cart.models import CartItem

"""Вьюха для ajax работы на странице товара
Описание:
-получает тарибуты товара через jQuery со страницы товара
-произваодит валидацию полученных данных
-вызывает метод создания или обновления еденицы товара
-формирует json с данными для обновления html страницы"""


@csrf_protect
def ajaxCart(request):
    postdata = request.POST.copy()
    form = ProductAddToCartForm(request, postdata)
    # cart_item = CartItem()
    add_item_html = ''
    data = {}
    if form.is_valid():  # тут происходит проверка на cookie в forms.py
        # Добавляем в корзину и делаем перенаправление на страницу с корзиной
        cart.add_to_cart(request)
        # product_item = Product.objects.get(slug=request.POST['product_slug'])
        # cart_item = CartItem.objects.get(product=product_item, cart_id=cart._cart_id(request))
        cart_products = cart.get_cart_items(request)
        global_quantity = cart.cart_distinct_item_count(request)

        """просто каждый раз строим карзину заново (это просто :-))"""
        add_item_html = u""
        for cart_item in cart_products:
            name = cart_item.name
            price = cart_item.price
            add_item_html = add_item_html + u"<div class='cart_items_prod'><img src='/media/%s' width='88' height='88'><div class='text_item'><p class='name_item'>%s</p><p>Цена: <i class='fa fa-rub'></i>%s</p><p id='quantity'>Колличество: %s</p></div></div>" %  (cart_item.get_default_image(), name, price, cart_item.quantity)

        data = simplejson.dumps({"add_item_html":add_item_html, "global_quantity":global_quantity})

    else:
        form = ProductAddToCartForm(request, postdata)

    return HttpResponse(data, mimetype="application/json")


def ajaxDelivery(request):
    data = {}
    current_delivery = cart.get_delivery(request)
    current_delivery.delivery_price = calculate_delivery_price(request.POST['text'], current_delivery.weight)
    current_delivery.save()
    # text = '<h4><strong>Параметры доставки:</strong></h4><p>Город: <span id="sity">%s</span></p>' \
    #        '<p>Вес посылки : <span id="weight_ajax">%s гр.</span></p>' \
    #        '<p>Стоимость доставки: <span id="price_ajax">%s руб.</span></p>' % (request.POST['text'],
    #                                                                              current_delivery.weight,
    #                                                                              current_delivery.delivery_price)
    data = simplejson.dumps({'city': request.POST['text'],
                             'price': str(current_delivery.delivery_price),
                             'weight': str(current_delivery.weight)})

    return HttpResponse(data, mimetype="application/json")
