from django import forms
from django.forms import ValidationError
from material.forms import ModelForm

from .models import Purchase


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


class NecessaryPriceQuoteForm(ModelForm):
    need_price_quote = forms.NullBooleanField(required=True)

    purchase_team_comment = forms.CharField(max_length=150,
                                            label="Purchase team comment")

    support_user = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    support_comment = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    class Meta(SupportForm.Meta):
        fields = SupportForm.Meta.fields + [
            'support_user', 'need_price_quote', 'purchase_team_comment']

    def clean(self):
        # Must be "== None" check instead; otherwise, condition would accept
        # for False boolean
        if self.cleaned_data['need_price_quote'] == None:
            raise ValidationError(
                {'need_price_quote': ["This field is required", ]})


class GetPriceQuoteForm(NecessaryPriceQuoteForm):
    need_price_quote = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    purchase_team_comment = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    class Meta(NecessaryPriceQuoteForm.Meta):
        fields = NecessaryPriceQuoteForm.Meta.fields + ['price_quoted',
                                                        'investigator_comment']


class ManagerApprovalForm(GetPriceQuoteForm):
    investigator_comment = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    price_quoted = forms.FloatField(widget=forms.Textarea(
        attrs={'readonly': True}))

    class Meta(GetPriceQuoteForm.Meta):
        fields = GetPriceQuoteForm.Meta.fields + [
            'manager_comment', 'manager_approval']

    def clean(self):
        if self.cleaned_data['manager_approval'] == None:
            raise ValidationError(
                {'manager_approval': ["This field is required", ]})
