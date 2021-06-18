from django import forms
from django.core import validators

# class CommentForm(forms.Form):
#     subject = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': 'عنوان نظر خود را بنویسید', 'class': 'input-ui pr-2'}),
#         label='عنوان نظر شما (اجباری)',
#         validators=[
#             validators.MaxLengthValidator(20, 'عنوان نباید بیشتر از 100 کارکتر باشد'),
#             validators.MinLengthValidator(4, 'عنوان نباید کمتر از 4 کارکتر باشد')
#         ]
#     )
#     comment = forms.CharField(
#         widget=forms.Textarea(
#             attrs={'rows': 5, 'placeholder': 'متن خود را بنویسید', 'class': 'input-ui pr-2 pt-2'}),
#         label='متن نظر شما (اجباری)'
#     )
#     advantage = forms.CharField(
#         widget=forms.MultipleHiddenInput(
#             attrs={'id': "advantage-input", 'class': 'input-ui pr-2 ui-input-field', 'autocomplete': "off", }),
#         label='نقاط قوت'
#     )

from django.forms import ModelForm
from eshop_comment.models import Comment, RateComment
from eshop_attribute.models import AttrProduct


class CommentForm(ModelForm):
    advantage = forms.CharField(widget=forms.MultipleHiddenInput(), required=False)
    disadvantage = forms.CharField(widget=forms.MultipleHiddenInput(), required=False)
    advice = forms.CharField(widget=forms.RadioSelect())

    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'advantage', 'disadvantage', 'advice']


class RateCommentForm(ModelForm):

    rate = forms.IntegerField(widget=forms.TextInput())

    class Meta:
        model = RateComment
        fields = ['rate']
