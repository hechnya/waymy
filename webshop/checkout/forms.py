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

REGIONS = [('АБАКАН', 'АБАКАН'),  ('АНАДЫРЬ', 'АНАДЫРЬ'),  ('АРХАНГЕЛЬСК', 'АРХАНГЕЛЬСК'),  ('АСТРАХАНЬ', 'АСТРАХАНЬ'),  ('БАРНАУЛ', 'БАРНАУЛ'),  ('БЕЛГОРОД', 'БЕЛГОРОД'),  ('БИРОБИДЖАН', 'БИРОБИДЖАН'),  ('БЛАГОВЕЩЕНСК', 'БЛАГОВЕЩЕНСК'),  ('БРЯНСК', 'БРЯНСК'),  ('ВЕЛИКИЙ НОВГОРОД', 'ВЕЛИКИЙ НОВГОРОД'),  ('ВЛАДИВОСТОК', 'ВЛАДИВОСТОК'),  ('ВЛАДИКАВКАЗ', 'ВЛАДИКАВКАЗ'),  ('ВЛАДИМИР', 'ВЛАДИМИР'),  ('ВОЛГОГРАД', 'ВОЛГОГРАД'),  ('ВОЛОГДА', 'ВОЛОГДА'),  ('ВОРОНЕЖ', 'ВОРОНЕЖ'),  ('ГОРНО-АЛТАЙСК', 'ГОРНО-АЛТАЙСК'),  ('ГРОЗНЫЙ', 'ГРОЗНЫЙ'),  ('ЕКАТЕРИНБУРГ', 'ЕКАТЕРИНБУРГ'),  ('ИВАНОВО', 'ИВАНОВО'),  ('ИЖЕВСК', 'ИЖЕВСК'),  ('ИРКУТСК', 'ИРКУТСК'),  ('ЙОШКАР-ОЛА', 'ЙОШКАР-ОЛА'),  ('КАЗАНЬ', 'КАЗАНЬ'),  ('КАЛИНИНГРАД', 'КАЛИНИНГРАД'),  ('КАЛУГА', 'КАЛУГА'),  ('КЕМЕРОВО', 'КЕМЕРОВО'),  ('КИРОВ', 'КИРОВ'),  ('КОСТРОМА', 'КОСТРОМА'),  ('КРАСНОДАР', 'КРАСНОДАР'),  ('КРАСНОЯРСК', 'КРАСНОЯРСК'),  ('КУРГАН', 'КУРГАН'),  ('КУРСК', 'КУРСК'),  ('КЫЗЫЛ', 'КЫЗЫЛ'),  ('ЛИПЕЦК', 'ЛИПЕЦК'),  ('МАГАДАН', 'МАГАДАН'),  ('МАЙКОП', 'МАЙКОП'),  ('МАХАЧКАЛА', 'МАХАЧКАЛА'),  ('МОСКВА', 'МОСКВА'),  ('МУРМАНСК', 'МУРМАНСК'),  ('НАЗРАНЬ', 'НАЗРАНЬ'),  ('НАЛЬЧИК', 'НАЛЬЧИК'),  ('НАРЬЯН-МАР', 'НАРЬЯН-МАР'),  ('НИЖНИЙ НОВГОРОД', 'НИЖНИЙ НОВГОРОД'),  ('НОВОСИБИРСК', 'НОВОСИБИРСК'),  ('ОМСК', 'ОМСК'),  ('ОРЕНБУРГ', 'ОРЕНБУРГ'),  ('ОРЁЛ', 'ОРЁЛ'),  ('ПЕНЗА', 'ПЕНЗА'),  ('ПЕРМЬ', 'ПЕРМЬ'),  ('ПЕТРОЗАВОДСК', 'ПЕТРОЗАВОДСК'),  ('ПЕТРОПАВЛОВСК-КАМЧАТСКИЙ', 'ПЕТРОПАВЛОВСК-КАМЧАТСКИЙ'),  ('ПСКОВ', 'ПСКОВ'),  ('РОСТОВ-НА-ДОНУ', 'РОСТОВ-НА-ДОНУ'),  ('РЯЗАНЬ', 'РЯЗАНЬ'),  ('САЛЕХАРД', 'САЛЕХАРД'),  ('САМАРА', 'САМАРА'),  ('САНКТ-ПЕТЕРБУРГ', 'САНКТ-ПЕТЕРБУРГ'),  ('САРАНСК', 'САРАНСК'),  ('САРАТОВ', 'САРАТОВ'),  ('СИМФЕРОПОЛЬ', 'СИМФЕРОПОЛЬ'),  ('СМОЛЕНСК', 'СМОЛЕНСК'),  ('СТАВРОПОЛЬ', 'СТАВРОПОЛЬ'),  ('СЫКТЫВКАР', 'СЫКТЫВКАР'),  ('ТАМБОВ', 'ТАМБОВ'),  ('ТВЕРЬ', 'ТВЕРЬ'),  ('ТОМСК', 'ТОМСК'),  ('ТУЛА', 'ТУЛА'),  ('ТЮМЕНЬ', 'ТЮМЕНЬ'),  ('УЛАН-УДЭ', 'УЛАН-УДЭ'),  ('УЛЬЯНОВСК', 'УЛЬЯНОВСК'),  ('УФА', 'УФА'),  ('ХАБАРОВСК', 'ХАБАРОВСК'),  ('ХАНТЫ-МАНСИЙСК', 'ХАНТЫ-МАНСИЙСК'),  ('ЧЕБОКСАРЫ', 'ЧЕБОКСАРЫ'),  ('ЧЕЛЯБИНСК', 'ЧЕЛЯБИНСК'),  ('ЧЕРКЕССК', 'ЧЕРКЕССК'),  ('ЧИТА', 'ЧИТА'),  ('ЭЛИСТА', 'ЭЛИСТА'),  ('ЮЖНО-САХАЛИНСК', 'ЮЖНО-САХАЛИНСК'),  ('ЯКУТСК', 'ЯКУТСК'),  ('ЯРОСЛАВЛЬ', 'ЯРОСЛАВЛЬ'),]

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
    # CHOICES = [('russian_post', 'Почта России')]
    # delivery = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'calc_delivery'}))
    region = forms.ChoiceField(choices=REGIONS, widget=forms.Select(attrs={'class': 'set_region'}))


class OneClickForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OneClickForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs = {'placeholder':'Ваш телефон'}
    product_name = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = OrderOneClick