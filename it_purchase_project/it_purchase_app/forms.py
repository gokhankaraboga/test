from django import forms
from material.forms import ModelForm
from viewflow.forms import ActivationDataForm
from .models import Purchase
from ..profile.models import Profile

class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = [
           'description',]
class SupportForm(ActivationDataForm):
    def __init__(self, *args, **kwargs):  # noqa D102
        kwargs.setdefault('prefix', '_viewflow_activation')
        super(SupportForm, self).__init__(*args, **kwargs)


    support_comment = forms.CharField(max_length=150,label="please support comment")

    class Meta:
        model = Purchase
        fields = ['support_comment',]


class PriceQuoteForm(ActivationDataForm):
    def __init__(self, *args, **kwargs):  # noqa D102
        kwargs.setdefault('prefix', '_viewflow_activation')
        super(PriceQuoteForm, self).__init__(*args, **kwargs)

    price_quote_required = forms.BooleanField()
    purchase_comment = forms.CharField(max_length=150,label="Purchase team comment")

    class Meta:
        model = Purchase
        fields = ['purchase_comment', 'price_quote_required']