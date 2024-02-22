from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker", "date"]
        widgets = {
            "ticker": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "date": forms.DateInput(
                attrs={"class": "form-control"}
            ),
        }