from django import forms
from store.models import *


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Enter Coupon Code",
    }))


