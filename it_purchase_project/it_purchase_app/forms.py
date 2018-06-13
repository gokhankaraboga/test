from django import forms
from django.forms import ValidationError
from material.forms import ModelForm, InlineFormSetField
from django.forms import inlineformset_factory
from .models import Purchase, PurchaseItem, BOOLEAN_CHOICES, NOT_DECIDED
from django.utils.translation import gettext_lazy as _


class PurchaseForm(ModelForm):
    items = InlineFormSetField(Purchase, PurchaseItem,
                               fields=['name', 'quantity'], extra=1)

    class Meta:
        model = Purchase
        fields = [
            'description', ]

    def clean(self):
        error_message = _("You have to specify one item at least")
        if self.formsets["items"].is_valid():
            for i in range(len(self.formsets["items"].cleaned_data)):
                if i not in self.formsets['items']._deleted_form_indexes:

                    item = self.formsets["items"].cleaned_data[i]

                    if not (item.get("name") and item.get('quantity')):
                        raise ValidationError(
                            error_message)
                    return
            raise ValidationError(
                error_message)


class PurchaseItemForm(ModelForm):
    name = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    quantity = forms.IntegerField(
        widget=forms.Textarea(attrs={"readonly": True}))

    class Meta:
        model = PurchaseItem
        fields = ['name', 'quantity']


class SupportForm(ModelForm):
    support_comment = forms.CharField(max_length=150,
                                      label=_("please support comment"))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    items = InlineFormSetField(
        formset_class=inlineformset_factory(Purchase, PurchaseItem,
                                            form=PurchaseItemForm,
                                            can_delete=False,
                                            extra=0, max_num=1))
    created_by = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    support_approval = forms.ChoiceField(choices=BOOLEAN_CHOICES, required=True)

    class Meta:
        model = Purchase
        fields = ['support_comment', 'description', 'support_approval']

    def clean(self):
        # Must be "== None" check instead; otherwise, condition would accept
        # for False boolean
        if self.cleaned_data['support_approval'] == NOT_DECIDED:
            raise ValidationError(
                {'support_approval': ["This field is required", ]})


class NecessaryPriceQuoteForm(ModelForm):
    need_price_quote = forms.ChoiceField(choices=BOOLEAN_CHOICES, required=True)

    purchase_team_comment = forms.CharField(max_length=150,
                                            label=_("Purchase team comment"))

    created_by = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    items = InlineFormSetField(
        formset_class=inlineformset_factory(Purchase, PurchaseItem,
                                            form=PurchaseItemForm,
                                            can_delete=False,
                                            extra=0, max_num=1))
    support_user = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    support_comment = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))
    support_approval = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': True}))

    currency_quoted = forms.CharField(max_length=150,
                                      label="Currency", required=False)
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
                _("Either you can fill both 'Currency' and 'Price Quoted' "
                "fields or omit both of them."))


class GetPriceQuoteForm(NecessaryPriceQuoteForm):
    items = InlineFormSetField(
        formset_class=inlineformset_factory(Purchase, PurchaseItem,
                                            form=PurchaseItemForm,
                                            can_delete=False,
                                            extra=0, max_num=1))
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
    items = InlineFormSetField(
        formset_class=inlineformset_factory(Purchase, PurchaseItem,
                                            form=PurchaseItemForm,
                                            can_delete=False,
                                            extra=0, max_num=1))
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
    items = InlineFormSetField(
        formset_class=inlineformset_factory(Purchase, PurchaseItem,
                                            form=PurchaseItemForm,
                                            can_delete=False,
                                            extra=0, max_num=1))
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
