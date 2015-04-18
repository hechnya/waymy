# -*- coding: utf-8 -*-
#!/usr/bin/env python
import datetime
import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import email_re
from django.utils.encoding import smart_unicode

from webshop import settings
from models import Order, OrderOneClick


class ContactForm(forms.ModelForm):

    # payment_method =  forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Order
        exclude = ('status', 'ip_address', 'user', 'transaction_id', 'delivery', 'cupon',)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        # переопределяем аттрибуты по умолчанию
        self.fields['payment_method'].widget = forms.HiddenInput()
        for field in self.fields:
            self.fields[field].widget.attrs['size'] = '20'

    def clean_phone(self):
        """Проверка телефонного номера (>10 цифр)"""
        phone = self.cleaned_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 11:
            raise forms.ValidationError(_(u"""
            Введите правильный телефон, например (8-920-351-21-21 или 89203512121)"""))
        return self.cleaned_data['phone']


def strip_non_numbers(data):
    """Удаляет все символы которые не являются числом
    >>> strip_non_numbers('988f2ds2')
    '98822'
    """
    non_numbers = re.compile('\D')
    return non_numbers.sub('', data)


class CheckoutForm(forms.ModelForm):
    """Форма оформления заказа"""
    class Meta:
        model = Order
        exclude = ('status', 'ip_address', 'user', 'transaction_id',)


class DeliveryForm(forms.Form):
    CHOICES = [('SPSurface', 'Small Packet Surface 25-40 дней'),
               ('SPSAL', 'Small Packet SAL 3-4 недели'),
               ('SPA', 'Small Packet Air 2-3 недели'),
               ('PS', 'Parcel Surface 25-30 дней'),
               ('EMS', 'EMS 7-10 дней'),]
    delivery = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'calc_delivery'}))


class OneClickForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OneClickForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs = {'placeholder':'Ваш телефон'}
    product_name = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = OrderOneClick