# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
import datetime
from django_mobile import set_flavour
from webshop.catalog import mobile

from webshop.cart import cart
from webshop.catalog.forms import ProductAddToCartForm, get_form_add_to_cart
from django.core.mail import send_mail
from webshop.catalog.models import *
from webshop.reviews.models import ReviewsProduct
from webshop.reviews.forms import ReviewProductForm
from webshop.catalog.forms import FormFront
from webshop.slider.models import Slider
from webshop.news.models import News
from webshop.pages.models import Page
from webshop.accounts.models import UserProfile


def index_view(request, template_name="catalog/index.html"):
    """Представление главной страницы"""

    # set_flavour('ipad')
    # определение устройства
    user_agent = request.META.get("HTTP_USER_AGENT")
    http_accept = request.META.get("HTTP_ACCEPT")
    if user_agent and http_accept:
        agent = mobile.UAgentInfo(userAgent=user_agent, httpAccept=http_accept)
        # устройство посетителя - новый смартфон (iPhone, Android, Windows Phone 7, и т.д.)
        if agent.detectTierIphone():
            device = u'mobile'
            template_name="mobile/catalog/index.html"
            # HttpResponseRedirect('/myapp/i/')
        # устройство посетителя - старый телефон
        if agent.detectMobileQuick():
            device = u'mobiled'
            template_name="mobile/catalog/index.html"
            # HttpResponseRedirect('/myapp/m/')
        if agent.detectTierTablet():
            device = u'tablet'
            template_name="tablet/catalog/index.html"
    # Для традиционных компьютеров и планшетов (iPad, Android, и т.д.)
    # return HttpResponseRedirect('/myapp/d/')

    page_title = _(u'Internet Magazine')
    products = Product.objects.all()
    for p in products:
        try:
            p.image = ProductImage.objects.get(product=p, default=True)
            p.volume = ProductVolume.objects.get(product=p, default=True)
        except Exception:
            p.image = "/media/products/images/none.png"

    reviews = Review.objects.all()

    #Далее вывод новостей
    news = News.objects.all()[:5]
    try:
        # frontpage = get_object_or_404(Page, is_main='True')
        frontpage = Page.objects.get(is_main='True')
    except Exception:
        frontpage = Page.objects.get(slug="404")

    if request.method == 'POST':
        form = FormFront(request.POST)
        subject = u'WayMy заявка от %s' % request.POST['name']
        message = u'телефон: %s \n Имя: %s' % (request.POST['phone'], request.POST['name'])
        if form.is_valid():
            send_mail(subject, message, 'teamer777@gmail.com', ['teamer777@icloud.com'], fail_silently=False)
            return HttpResponseRedirect('/')
        else:
            form = FormFront({'phone': u'Введите свой телефон',})
    else:
        form = FormFront()

    # Функция locals получает все поля словаря
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

"""функция фильтрации повторяющихся позиций"""
def sortAndUniq(input):
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    output.sort()
    return output

def category_view(request, category_slug, template_name="catalog/category.html"):
    """Представление для просмотра конкретной категории"""
    c = get_object_or_404(Category.active, slug=category_slug)

    # products = Product.objects.all()
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
        request.breadcrumbs([('%s' % parent_cat.name, parent_url), ('%s' % c.name,request.path_info)])

    for p in products:
        try:
            p.image_url = ProductImage.objects.get(product=p, default=True).url
            p.volume = ProductVolume.objects.get(product=p, default=True)
        except Exception:
            p.image_url = "/media/products/images/none.png"
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
        products = list(set(products)) #удаляем повторы

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
    """Представление для просмотра конкретного продукта"""

    p = get_object_or_404(Product, slug=product_slug)
    try:
        attachedProducts = p.itemsAttached.all()
        for attachedP in attachedProducts:
            try:
                attachedP.image_url = ProductImage.objects.get(product=attachedP, default=True).url
                attachedP.volume = ProductVolume.objects.get(product=attachedP, default=True)
            except Exception:
                attachedP.image_url = "/media/products/images/none.png"
    except:
        None

    reviews = ReviewsProduct.objects.filter(product=p)

    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
        user.have_profile = True
    except:
        user.have_profile = False


    # breadcrumbs
    cat = p.categories.all()
    c = get_object_or_404(Category, id=cat[0].id)
    if c.level == 0:
        request.breadcrumbs([('%s' % c.name,request.path_info), ('%s' % p.name, request.path_info)])
    else:
        parent_cat = Category.objects.get(id=c.parent.id)
        parent_url = parent_cat.get_absolute_url()
        request.breadcrumbs([('%s' % parent_cat.name, parent_url), ('%s' % c.name, c.get_absolute_url()), ('%s' % p.name, request.path_info)])


    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description

    # достаем все фотки + дефлтную
    try:
        product_image = ProductImage.objects.get(product=p, default=True)
        images = ProductImage.objects.filter(product=p)
    except Exception:
        print "Image for product #%s not found" % p.id

    characteristics = Characteristic.objects.filter(product=p)

    # достаем основные атрибуты
    try:
        atrs_default = ProductVolume.objects.get(product=p, default=True)
        atrs = ProductVolume.objects.filter(product=p)
    except Exception:
        print  u'Основные атрибуты продукта %s не найдены' % p.name

    # Проверка HTTP метода
    if request.method == 'POST':
        # Добавление в корзину, создаем связанную форму
        postdata = request.POST.copy()

        if postdata.has_key('review'):
            # form2 = ReviewProductForm(request, postdata)
            review = ReviewsProduct()
            review.text = postdata.get('text', '')
            review.userProfile = UserProfile.objects.get(user=request.user)
            review.product = p
            review.date = datetime.date.today()
            review.save()

            return HttpResponseRedirect('/product/%s' % product_slug)

        else:

            form = ProductAddToCartForm(request, postdata)
            # form = get_form_add_to_cart(request, postdata)
            # form2 = ProductOneClickForm(request.POST or None)
            # Проверка что отправляемые данные корректны
            if form.is_valid():
                # Добавляем в корзину и делаем перенаправление на страницу с корзиной
                cart.add_to_cart(request)
                # Если cookies работают, читаем их
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                # url = urlresolvers.reverse('show_cart')
                return HttpResponseRedirect('/product/%s' % product_slug)
            # if form2.is_valid():
            #     phone = request.POST['phone']
            #     text = u'Заявка на товар %s \n телефон: %s' % (page_title, phone)
            #     send_mail('в 1 клик', text, 'teamer777@gmail.com', ['greenteamer@bk.ru'], fail_silently=False)
            #     return HttpResponseRedirect('/product/%s/' % product_slug)
            else:
                form = ProductAddToCartForm(request, postdata)
                # form = get_form_add_to_cart(request, postdata)
                error = form.errors
                return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
                # return HttpResponseRedirect('/product/%s' % product_slug)
                # return render(request, template_name, {
                #     'form': form,
                #     'error': form.errors,
                # })

    else:
        # Если запрос GET, создаем не привязанную форму. request передаем в kwarg
        form = ProductAddToCartForm(request=request, label_suffix=':')
        form2 = ReviewProductForm()
        # form = get_form_add_to_cart(request, postdata=None)
        # form2 = ProductOneClickForm()
    # form = get_form_add_to_cart(request)
    # Присваиваем значению скрытого поля чистое имя продукта
        form.fields['product_slug'].widget.attrs['value'] = product_slug


    # form2.fields['product_name'].widget.attrs['value'] = p.name
    # Устанавливаем тестовые cookies при первом GET запросе
    request.session.set_test_cookie()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))
