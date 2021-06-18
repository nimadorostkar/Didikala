from django import forms
from django.core import validators
from django.forms import ModelForm, TextInput, Textarea

from eshop_contact.models import ContactMessage


class ContactUSForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام و نام‌خانوادگی خود را وارد کنید', 'class': 'form-control'}),
        label='نام و نام‌خانوادگی',
        validators=[
            validators.MaxLengthValidator(20, 'نام کاربری نباید بیشتر از 20 کارکتر باشد'),
            validators.MinLengthValidator(4, 'نام کاربری نباید کمتر از 4 کارکتر باشد')
        ]
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'ایمیل خود را وارد کنید', 'class': 'form-control'}),
        label='ایمیل'
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'عنوان پیام', 'class': 'form-control'}),
        label='موضوع پیام',
        validators=[
            validators.MaxLengthValidator(20, 'عنوان نباید بیشتر از 100 کارکتر باشد'),
            validators.MinLengthValidator(4, 'عنوان نباید کمتر از 4 کارکتر باشد')
        ]
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 8, 'placeholder': 'پیام خود را بنویسید', 'class': 'form-control '}),
        label='پیام'
    )
