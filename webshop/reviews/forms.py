# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _

from webshop.reviews.models import ReviewsProduct

class ReviewProductForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))


    # feel = forms.ModelChoiceField(queryset=FeelName.objects.all(),
    #                               widget=forms.Select(attrs={'id':'name'}), required=True)
    # feel = forms.ModelChoiceField(widget=forms.Select(attrs={'id':'name'}), required=True)






    # product_slug = forms.CharField(widget=forms.HiddenInput())
    # class Meta:
    #     model = OrderOneClick
        # exclude = ('product_name')
        # widgets = {
        #     'phone': forms.TextInput(attrs={'placeholder': "Ваш телефон"}),
        #     'description': forms.Textarea(
        #         attrs={'placeholder': 'Enter description here'}),
        # }


