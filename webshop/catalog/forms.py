# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _

from models import Product, Category, FeelName
from webshop.checkout.models import OrderOneClick


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()

    def clean_price(self):
        """Проверка поля цена"""
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError(_(u'Price must be greater than zero.'))
        return self.cleaned_data['price']

    def __init__(self, *args, **kwds):
        super(ProductAdminForm, self).__init__(*args, **kwds)
        self.fields['categories'].queryset = Category.objects.order_by('created_at')

def feelList_request():
    feelList = FeelName.objects.all()
    dictionary = {}
    for feel in feelList:
        dictionary[feel.id] = '%s' % feel.name

    return dictionary


def get_form_add_to_cart(request, postdata):
    if request.method == 'POST':
        product = Product.objects.get(slug=postdata.get('product_slug', ''))
        feels_product = product.feel
        test = 123
    form = ProductAddToCartForm(request, postdata)
    return form


class ProductAddToCartForm(forms.Form):
    """Форма добавления товара в корзину"""

    # FEEL_CHOICES = feelList_request()

    # feel = forms.ModelChoiceField(queryset=FeelName.objects.all(),
    #                               widget=forms.Select(attrs={'id':'name'}), required=True)
    # feel = forms.ModelChoiceField(widget=forms.Select(attrs={'id':'name'}), required=True)
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size': '2',
                                                                'value': '1', 'class': 'quantity', 'maxlength': '5'}),
        error_messages={'invalid': _(u'Please enter a valid quantity.')},
        min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request=None, *args, **kwargs):
        """
        Переопределение метода __init__ по умолчанию для получения словаря request
        нужен для проверки работы cookies
        """

        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)
        # self.fields['feel'].queryset = Y.objects.filter(id_X=x)
        # self.fields['feel'].queryset = Product.objects.get(slug=self.product_slug)
        # obj = self.fields['product_slug']
        # test = 123



    def clean(self):
        """Проверка что cookies в браузере включены"""
        if self.request:
            if not self.request.session.test_cookie_worked() and 'cookie_tested' not in self.request.session:
                # self.request.session.delete_test_cookie()
                self.request.session['cookie_tested'] = True
                # raise forms.ValidationError(_(u'Cookies must be enabled.'))
        return self.cleaned_data


class ProductOneClickForm(forms.ModelForm):
    # phone = forms.CharField(label=u'Ваш телефон (обязательно)', max_length=255)
    # product_slug = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = OrderOneClick
        exclude = ()
        # widgets = {
        #     'phone': forms.TextInput(attrs={'placeholder': "Ваш телефон"}),
        #     'description': forms.Textarea(
        #         attrs={'placeholder': 'Enter description here'}),
        # }

class FormFront(forms.Form):

    name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': u'Ваше имя'}))
    phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': u'Ваш телефон'}))

    # name = forms.CharField(max_length=100)
    # phone = forms.CharField(max_length=100)

    # def __init__(self, request=None, *args, **kwargs):
    #     """
    #     Переопределение метода __init__ по умолчанию для получения словаря request
    #     нужен для проверки работы cookies
    #     """
    #     self.request = request
    #     super(FormFront, self).__init__(*args, **kwargs)
    #
    # def clean(self):
    #     """Проверка что cookies в браузере включены"""
    #     if self.request:
    #         if not self.request.session.test_cookie_worked():
    #             raise forms.ValidationError(_(u'Cookies must be enabled.'))
    #     return self.cleaned_data