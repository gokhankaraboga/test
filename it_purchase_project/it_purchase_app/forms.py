from django import forms
from django.forms import ValidationError
from material.forms import ModelForm

from .models import Purchase, BOOLEAN_CHOICES, NOT_DECIDED


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

    support_approval = forms.ChoiceField(choices=BOOLEAN_CHOICES, required=True)


    class Meta:
        model = Purchase
        fields = ['support_comment', 'description','support_approval']

    def clean(self):
        # Must be "== None" check instead; otherwise, condition would accept
        # for False boolean
        if self.cleaned_data['support_approval'] == NOT_DECIDED:
            raise ValidationError(
                {'support_approval': ["This field is required", ]})

class NecessaryPriceQuoteForm(ModelForm):
    need_price_quote = forms.ChoiceField(choices=BOOLEAN_CHOICES, required=True)

    purchase_team_comment = forms.CharField(max_length=150,
                                            label="Purchase team comment")

    created_by = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    support_user = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    support_comment = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    support_approval = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    currency_quoted = forms.CharField(max_length=150,
                                      label="Currency",required=False)
    price_quoted = forms.FloatField(required=False)

    class Meta(SupportForm.Meta):
        fields = SupportForm.Meta.fields + [
            'need_price_quote', 'purchase_team_comment',
            'price_quoted', 'currency_quoted']

    def clean(self):
        currency = self.cleaned_data["currency_quoted"]
        price = self.cleaned_data["price_quoted"]

        if self.cleaned_data['need_price_quote'] == NOT_DECIDED:
            raise ValidationError(
                {'need_price_quote': ["This field is required", ]})

        if bool(currency) != bool(price):
            raise ValidationError(
                "Either you can fill both 'Currency' and 'Price Quoted' fields or omit both of them.")


class GetPriceQuoteForm(NecessaryPriceQuoteForm):
    need_price_quote = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    purchase_team_comment = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    price_quoted = forms.FloatField(required=True)
    currency_quoted = forms.CharField(max_length=150,
                                      label="Currency")
    investigator_comment = forms.CharField(required=False)
    purchase_team_user = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    class Meta(NecessaryPriceQuoteForm.Meta):
        fields = NecessaryPriceQuoteForm.Meta.fields + ['price_quoted',
                                                        'investigator_comment',
                                                        'currency_quoted']


class SuperiorApprovalForm(GetPriceQuoteForm):
    # TODO investigator_comment should be hidden input depending on conditions
    investigator_comment = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}), required=False)
    price_quoted = forms.FloatField(widget=forms.Textarea(
        attrs={'readonly': True}))
    superior_approval = forms.ChoiceField(choices=BOOLEAN_CHOICES,
                                          required=True)
    purchase_investigator_user = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}), required=False)
    currency_quoted = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    class Meta(GetPriceQuoteForm.Meta):
        fields = GetPriceQuoteForm.Meta.fields + [
            'superior_comment', 'superior_approval']

    def clean(self):
        if self.cleaned_data['superior_approval'] == NOT_DECIDED:
            raise ValidationError(
                {'superior_approval': ["This field is required", ]})


class ProceedPurchaseForm(SuperiorApprovalForm):
    superior_user = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    superior_approval = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    superior_comment = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    purchase_confirmation_comment = forms.CharField(max_length=150,
                                                    label="Purchase "
                                                          "Confirmation "
                                                          "comment")
