from django import forms
from material.forms import ModelForm

from .models import Purchase


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = [
           'description',
        ]

    # def clean(self):
    #     start_date = self.cleaned_data.get("start_date")
    #     end_date = self.cleaned_data.get("end_date")
    #     if end_date and start_date and end_date < start_date:
    #         self._errors["end_date"] = "*"
    #         raise forms.ValidationError(
    #             "End date should be equal or greater than  start date."
    #         )
