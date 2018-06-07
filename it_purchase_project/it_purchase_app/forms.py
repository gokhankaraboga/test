from django import forms
from django.forms import ValidationError
from material.forms import ModelForm

from .models import Purchase, BOOLEAN_CHOICES


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = [
            'description', ]


class SupportForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     self.created_by = kwargs.pop("created_by")
    #     kwargs["initial"]["created_by"] =  self.created_by
    #
    #     # self.initial["created_by"] = self.created_by.username
    #     super(SupportForm, self).__init__(*args, **kwargs)
    support_comment = forms.CharField(max_length=150,
                                      label="please support comment")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    created_by = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    class Meta:
        model = Purchase
        fields = ['support_comment', 'description', ]


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

    price_quoted = forms.FloatField(required=False)

    class Meta(SupportForm.Meta):
        fields = SupportForm.Meta.fields + [
            'need_price_quote', 'purchase_team_comment',
            'price_quoted']

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
    price_quoted = forms.FloatField(required=True)
    investigator_comment = forms.CharField(required=False)
    purchase_team_user = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    class Meta(NecessaryPriceQuoteForm.Meta):
        fields = NecessaryPriceQuoteForm.Meta.fields + ['price_quoted',
                                                        'investigator_comment']


class ManagerApprovalForm(GetPriceQuoteForm):
    # TODO investigator_comment should be hidden input depending on conditions
    investigator_comment = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}), required=False)
    price_quoted = forms.FloatField(widget=forms.Textarea(
        attrs={'readonly': True}))
    manager_approval = forms.ChoiceField(choices=BOOLEAN_CHOICES, required=True)

    purchase_investigator_user =  forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    class Meta(GetPriceQuoteForm.Meta):
        fields = GetPriceQuoteForm.Meta.fields + [
            'manager_comment', 'manager_approval']

    def clean(self):
        if self.cleaned_data['manager_approval'] == 'Not Decided':
            raise ValidationError(
                {'manager_approval': ["This field is required", ]})
