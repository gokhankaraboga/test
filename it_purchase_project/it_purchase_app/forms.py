from django import forms
from material.forms import ModelForm
from viewflow.forms import ActivationDataForm
from .models import Purchase, BOOLEAN_CHOICES
from django.utils.translation import gettext as _
from django.forms import ValidationError


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = [
            'description', ]


class SupportForm(ModelForm):
    support_comment = forms.CharField(max_length=150,
                                      label="please support comment")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    created_by = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    class Meta:
        model = Purchase
        fields = ['support_comment', 'description', 'created_by']


class PriceQuoteForm(ModelForm):
    need_price_quote = forms.NullBooleanField(required=True)

    purchase_team_comment = forms.CharField(max_length=150,
                                            label="Purchase team comment")

    support_comment = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    created_by = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    support_user = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    class Meta:
        model = Purchase
        fields = ['support_comment', 'description', 'created_by',
                  'support_user', 'need_price_quote', 'purchase_team_comment']

    def clean(self):
        if self.cleaned_data['need_price_quote'] == None:
            raise ValidationError(
                {'need_price_quote': ["This field is required", ]})
