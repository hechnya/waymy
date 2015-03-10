# -*- coding: utf-8 -*-
#!/usr/bin/env python
import decimal
import random

from django.shortcuts import get_object_or_404

from webshop.catalog.models import *
from webshop.checkout.models import Delivery
from webshop.cart.models import CartItem


def _cart_id(request):
    """
      Получение id корзины из cookies для пользователя,
      или установка новых cookies если не существуют
      _модификатор для видимости в пределах модуля
      """
    # if request.session.get(CART_ID_SESSION_KEY, '') == '':
    #     request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    # return request.session[CART_ID_SESSION_KEY]


def add_to_cart(request):
    """Добавление товара в корзину"""
    postdata = request.POST.copy()

    # Получаем чистое имя товара, возвращает пустую строку если нет
    product_slug = postdata.get('product_slug', '')

    # Получаем количество добавлеых товаров, возрат 1 если нет
    quantity = postdata.get('quantity', 1)

    # получаем набор атрибутов
    atr_value = postdata.get('atr_value', '')
    atributes = ProductVolume.objects.get(id=atr_value)

    # получаем вкус
    feel = postdata.get('feel', '')
    if feel == '':
        feel = None

    # Получаем товар, или возвращаем ошибку "не найден" если его не существует
    p = get_object_or_404(Product, slug=product_slug)

    # Получаем товары в корзине
    cart_products = get_cart_items(request)
    cupon = get_cupon(request)
    product_in_cart = False

    # Проверяем что продукт уже в корзине
    for cart_item in cart_products:
        if (cart_item.product.id == p.id) and ((cart_item.feel_id == feel) or ('%s' % cart_item.feel_id == feel)) and (cart_item.atributes == atributes):
            # Обновляем количество если найден
            cart_item.augment_quantity(quantity)
            product_in_cart = True

    if not product_in_cart:
        # Создаем и сохраняем новую корзину
        ci = CartItem()
        ci.product = p
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.cupon = cupon

        ci.atributes = atributes

        try:
            feelProduct = get_object_or_404(FeelName, id=feel)
        except Exception:
            feelProduct = None
        ci.feel = feelProduct


        ci.save()


def get_cart_items(request):
    """Получение всех товаров для текущей корзины"""
    return CartItem.objects.filter(cart_id=_cart_id(request))

def get_cupon(request):
    cart_items = get_cart_items(request)
    cupon = Cupon.objects.get(identifier='zero')
    if cart_items:
        for item in cart_items:
            cupon = item.cupon
    return cupon