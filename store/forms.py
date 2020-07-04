from django import forms
from store.models import *


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Enter Coupon Code",
    }))

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("name","contact","city","landmark","state","alternative_no","pin","address_type")

