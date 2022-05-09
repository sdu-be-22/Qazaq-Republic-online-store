from django import forms

from .models import *


# class CheckoutForm(forms.Form):
#     address = forms.CharField(max_length=255, null=True)
#     city = forms.CharField(max_length=255, null=True)
#     zipcode = forms.CharField(max_length=255, null=False)
#     cc_number = CardNumberField(label='Card Number')
#     cc_expiry = CardExpiryField(label='Expiration Date')
#     cc_code = SecurityCodeField(label='CVV/CVC')
