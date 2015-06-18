# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
import datetime
from webshop.catalog import mobile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from webshop.catalog.forms import ProductAddToCartForm, FormFront
from webshop.reviews.forms import ReviewProductForm
from webshop.checkout.forms import OneClickForm
from webshop.catalog.models import *
from webshop.reviews.models import ReviewsProduct
from webshop.news.models import News
from webshop.pages.models import Page
from webshop.accounts.models import UserProfile
from webshop.checkout.models import OrderOneClick
from webshop.pages.models import MetaInPages


def change_template_for_device(request, template_name):

    # определение устройства
    user_agent = request.META.get("HTTP_USER_AGENT")
    http_accept = request.META.get("HTTP_ACCEPT")
    trigger_for_mobile = False
    device = ''
    if user_agent and http_accept:
        agent = mobile.UAgentInfo(
            userAgent=user_agent, httpAccept=http_accept)

        if agent.detectTierIphone():
            """ устройство посетителя - новый смартфон
            (iPhone, Android, Windows Phone 7, и т.д.)"""
            device = 'mobile'
            template_name = "%s/%s" % (device, template_name)
            trigger_for_mobile = True

        if agent.detectMobileQuick() and not trigger_for_mobile:
            """HttpResponseRedirect('/myapp/i/')
            устройство посетителя - старый телефон"""
            device = 'mobiled'
            template_name = "mobile/%s" % template_name

        if agent.detectTierTablet():
            device = 'tablet'
            template_name = "%s/%s" % (device, template_name)

    dev_info = {'template_name': template_name, 'device': device}

    return dev_info


def index_view(request, template_name="catalog/index.html"):
    """Представление главной страницы"""

    # просто меняем шаблон в зависимости от устройства
    # TODO: подумать как не вызывать в каждой вьюхе этот метод
    template_name = change_template_for_device(request, template_name)['template_name']
    device = change_template_for_device(request, template_name)['device']

    page_title = u'Главная'
    products = Product.objects.all()
    for p in products:
        try:
            p.image = ProductImage.objects.get(product=p, default=True)
            p.volume = ProductVolume.objects.get(product=p, default=True)
        except Exception:
            p.image = "/media/products/images/none.png"
        """достаем основные атрибуты"""
        try:
            p.atrs_default = ProductVolume.objects.get(product=p, default=True)
            p.atrs = ProductVolume.objects.filter(product=p)
        except Exception:
            print u'Основные атрибуты продукта %s не найдены' % p.name

    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    reviews = Review.objects.all()

    #Далее вывод новостей
    news = News.objects.all()[:5]
    try:
        frontpage = Page.objects.get(is_main='True')
    except Exception:
        frontpage = Page()
        frontpage.name = u"Главная станица"
        frontpage.slug = "main"
        frontpage.is_main = True
        frontpage.save()

    # if request.method == 'POST':
    #     form = FormFront(request.POST)
    #     subject = u'WayMy заявка от %s' % request.POST['name']
    #     message = u'телефон: %s \n Имя: %s' % (
    #         request.POST['phone'], request.POST['name'])

    #     if form.is_valid():
    #         send_mail(
    #             subject, message, 'teamer777@gmail.com',
    #             ['teamer777@icloud.com'], fail_silently=False)

    #         return HttpResponseRedirect('/')
    #     else:
    #         form = FormFront({'phone': u'Введите свой телефон', })
    # else:
    form = FormFront()

    # Функция locals получает все поля словаря
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


def sortAndUniq(input):
    """функция фильтрации повторяющихся позиций"""
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    output.sort()
    return output


def category_view(
        request, category_slug, template_name="catalog/category.html"):
    """Представление для просмотра конкретной категории"""
    try:
        meta_object = MetaInPages.objects.get(link=request.path)
    except:
        pass
    c = get_object_or_404(Category.active, slug=category_slug)
    device = change_template_for_device(request, template_name)['device']
    products = []
    if c.level == 0:
        loop_category = Category.objects.filter(tree_id=c.tree_id)
        request.breadcrumbs('%s' % c.name, request.path_info)

        for category in loop_category:
            products_subcategory = category.product_set.all()

            for product in products_subcategory:
                products.append(product)

        """фильтруем повторяющиеся позиции"""
        products = sortAndUniq(products)

    else:
        products = c.product_set.all()
        parent_cat = Category.objects.get(id=c.parent.id)
        parent_url = parent_cat.get_absolute_url()
        request.breadcrumbs([
            ('%s' % parent_cat.name, parent_url),
            ('%s' % c.name, request.path_info)
        ])

    for p in products:
        try:
            p.image_url = ProductImage.objects.get(product=p, default=True).url
            p.volume = ProductVolume.objects.get(product=p, default=True)
        except Exception:
            p.image_url = "/media/products/images/none.png"
        """достаем основные атрибуты"""
        try:
            p.atrs_default = ProductVolume.objects.get(product=p, default=True)
            p.atrs = ProductVolume.objects.filter(product=p)
        except Exception:
            print u'Основные атрибуты продукта %s не найдены' % p.name

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


def sale_view(request, template_name="", type=""):
    """Представление для просмотра скидок"""
    if type == 'sale':
        request.breadcrumbs(u'Скидки', request.path_info)
        page_name = 'Скидки - горячая цена'
        sale_arts = ProductVolume.objects.exclude(new_price=0.00)
        products = []
        for p in sale_arts:
            prod = Product.objects.get(id=p.product_id)
            products.append(prod)
        products = list(set(products))  # удаляем повторы

    else:
        request.breadcrumbs(u'Новинки', request.path_info)
        page_name = 'Новинки!'
        products = Product.objects.filter(is_new=True)
    for p in products:
        try:
            p.image_url = ProductImage.objects.get(product=p, default=True).url
        except Exception:
            p.image_url = "/media/products/images/none.png"
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


@csrf_protect
def product_view(request, product_slug, template_name="catalog/product.html"):
    """представление для конкретного товара
    достаем объект, характеристики, все фотки + дефолтную"""
    device = change_template_for_device(request, template_name)['device']
    p = get_object_or_404(Product, slug=product_slug)
    try:
        product_image = ProductImage.objects.get(product=p, default=True)
        images = ProductImage.objects.filter(product=p)
    except Exception:
        print "Image for product #%s not found" % p.id
    """достаем основные атрибуты"""
    try:
        atrs_default = ProductVolume.objects.get(product=p, default=True)
        atrs = ProductVolume.objects.filter(product=p)
    except Exception:
        print u'Основные атрибуты продукта %s не найдены' % p.name
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
        user.have_profile = True
    except:
        user.have_profile = False
    reviews = ReviewsProduct.objects.filter(product=p)
    """Достаем присоединенные товары и их картинки"""
    try:
        attachedProducts = p.itemsAttached.all()
        for attachedP in attachedProducts:
            try:
                attachedP.image_url = ProductImage.objects.get(
                    product=attachedP, default=True).url
                attachedP.volume = ProductVolume.objects.get(
                    product=attachedP, default=True)
            except Exception:
                attachedP.image_url = "/media/products/images/none.png"
    except:
        None
    """хлебные крошки"""
    cat = p.categories.all()
    c = get_object_or_404(Category, id=cat[0].id)
    if c.level == 0:
        request.breadcrumbs([
            ('%s' % c.name, request.path_info),
            ('%s' % p.name, request.path_info)
        ])

    else:
        parent_cat = Category.objects.get(id=c.parent.id)
        parent_url = parent_cat.get_absolute_url()
        request.breadcrumbs([
            ('%s' % parent_cat.name, parent_url),
            ('%s' % c.name, c.get_absolute_url()),
            ('%s' % p.name, request.path_info)
        ])

    if request.method == 'POST':
        # Добавление в корзину, создаем связанную форму
        postdata = request.POST.copy()
        if 'review' in postdata:
            # form2 = ReviewProductForm(request, postdata)
            review = ReviewsProduct()
            review.text = postdata.get('text', '')
            review.userProfile = UserProfile.objects.get(user=request.user)
            review.product = p
            review.date = datetime.date.today()
            review.save()
            return HttpResponseRedirect('/product/%s' % product_slug)
        elif 'one_click' in postdata:
            form3 = OneClickForm(request.POST)
            form3.product_name = p.name
            if form3.is_valid():
                subject = u'WayMy заявка в 2 клика'
                message = u'телефон: %s \n Продукт: %s' % (
                    request.POST['phone'], request.POST['product_name'])

                send_mail(
                    subject, message, 'teamer777@gmail.com',
                    ['teamer777@icloud.com'], fail_silently=False)

                return HttpResponseRedirect('/product/%s' % product_slug)
    else:
        form = ProductAddToCartForm(request=request, label_suffix=':')
        form2 = ReviewProductForm()
        one_click_item = OrderOneClick(product_name=p.name)
        form3 = OneClickForm(instance=one_click_item)
    request.session.set_test_cookie()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))
