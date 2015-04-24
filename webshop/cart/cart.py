# -*- coding: utf-8 -*-
#!/usr/bin/env python
import decimal
import random

from django.shortcuts import get_object_or_404

from webshop.catalog.models import *
from webshop.checkout.models import Delivery
from webshop.cart.models import CartItem
from webshop.cart.delivery import calculate_delivery_price


CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):
    """
      Получение id корзины из cookies для пользователя,
      или установка новых cookies если не существуют
      _модификатор для видимости в пределах модуля
      """
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    """Генерация уникального id корзины который будет хранится в cookies"""
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters) - 1)]
    return cart_id


def get_cart_items(request):
    """Получение всех товаров для текущей корзины"""
    return CartItem.objects.filter(cart_id=_cart_id(request))


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
    # cupon = get_cupon(request)
    product_in_cart = False

    # Проверяем что продукт уже в корзине
    for cart_item in cart_products:
        if (cart_item.product.id == p.id) and ((cart_item.feel_id == feel) or ('%s' % cart_item.feel_id == feel)) and (cart_item.atributes == atributes):
            # Обновляем количество если найден
            cart_item.augment_quantity(quantity)
            product_in_cart = True
            return cart_item

    if not product_in_cart:
        # Создаем и сохраняем новую корзину
        ci = CartItem()
        ci.product = p
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        # ci.cupon = cupon

        ci.atributes = atributes
        try:
            feelProduct = get_object_or_404(FeelName, id=feel)
        except Exception:
            feelProduct = None
        ci.feel = feelProduct

        ci.save()
        return ci


def cart_distinct_item_count(request):
    """Возвращает общее количество товаров в корзине (количество однотипных товаров)"""
    # return get_cart_items(request).count()
    """возвращаем колличество всех товаров в корзине ... метод len или count не подходят потому что не считаюст quantity каждого cart_item"""
    quantity = 0
    for item in get_cart_items(request):
        quantity = quantity + item.quantity
    return quantity


def get_single_item(request, item_id):
    """Получаем конкретный товар в корзине"""
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))


def update_cart(request):
    """Обновляет количество отдельного товара"""
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
    #else:
    #TODO: добавить предупреждение
    #    remove_from_cart(request)


def update_cupon_cart(request):
    cart_products = get_cart_items(request)
    postdata = request.POST.copy()
    cupon_code ='%s' % postdata['cupon']
    try:
        cupon_true = Cupon.objects.get(identifier=cupon_code)
    except Exception:
        cupon_true = Cupon.objects.get(identifier='zero')
    for cart_item in cart_products:
        cart_item.cupon = cupon_true
        cart_item.save()


def get_cupon(request):
    cart_items = get_cart_items(request)
    cupon = Cupon.objects.get(identifier='zero')
    if cart_items:
        for item in cart_items:
            cupon = item.cupon
    return cupon


def remove_from_cart(request):
    """Удаляет выбранный товар из корзины"""
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


def cart_subtotal(request):
    """Получение суммарной стоимости всех товаров"""
    cart_total = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += cart_item.price * cart_item.quantity
    return cart_total


def cart_delivery_total(request):
    delivery = get_current_delivery(request)
    return delivery.delivery_price


def cart_total(request):
    total = cart_subtotal(request) + cart_delivery_total(request)
    return total


def cart_gift_add(request):
    """добавляем подарок"""
    gifts = GiftPrice.objects.all()
    cart_total = cart_subtotal(request)
    # result = GiftPrice()
    for gift in gifts:
        if gift.price < cart_total:

            result = gift

            try:
                result.image_url = GiftPrice.objects.get(product=gift, default=True).url
            except Exception:
                result.image_url = "/media/products/images/none.png"

            return result


def is_empty(request):
    """Если корзина пустая возвращаем True"""
    return cart_distinct_item_count(request) == 0


def empty_cart(request):
    """Очищает корзину покупателя"""
    user_cart = get_cart_items(request)
    user_cart.delete()


                                                    ### ДОСТАВКА ###
# подчсет доставки
# сохраняем доставку и возвращием во вьюху
def get_delivery(request):
    delivery = get_current_delivery(request)
    delivery.gift = cart_gift_add(request)
    delivery.weight = calculate_delivery_weight(request, delivery.gift)
    # получаем стоимость доставки
    return delivery


# получаем текущую доставку или создаем новую
def get_current_delivery(request):
    try:
        delivery = Delivery.objects.get(cart_id_delivery=_cart_id(request))
    except Exception:
        delivery = Delivery()
        delivery.cart_id_delivery = '%s' % _cart_id(request)
    return delivery


# считаем вес доставки
def calculate_delivery_weight(request, gift):
    items = get_cart_items(request)
    delivery_weight = 0

    for item in items:
        delivery_weight += item.atributes.weight * item.quantity

    if gift:
        gift_weight = gift.weight
        delivery_weight = delivery_weight + gift_weight

    delivery_weight = delivery_weight + 200

    return delivery_weight


def add_to_cart_ajax(request, tovar, quantity, value):
    """Добавление товара в корзину"""

    # Получаем чистое имя товара, возвращает пустую строку если нет
    product_slug = tovar

    # Получаем количество добавлеых товаров, возрат 1 если нет
    quantity = quantity

    # получаем набор атрибутов
    atributes = ProductVolume.objects.get(id=value)

    # получаем вкус
    feel = ''
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
