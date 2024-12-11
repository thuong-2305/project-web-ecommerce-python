from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:100%', 'placeholder':'Full name'}), required=True)
    shipping_phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:100%', 'placeholder':'Email'}), required=True)
    shipping_address = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:100%', 'placeholder':'Address'}), required=True)
    shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:100%', 'placeholder':'State'}), required=False)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_phone', 'shipping_address', 'shipping_state']

        exclude = ['user']

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:100%', 'placeholder':"Cardholder's Name"}), required=True)
    card_number =forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:100%', 'placeholder':'Card Number'}), required=True)
    card_exp_date = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:100%', 'placeholder':'Expiration Date'}), required=True)
    card_cvv_number =forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:100%', 'placeholder':'CVV'}), required=True)
    card_address = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:100%', 'placeholder':'Billing Address'}), required=True)
    card_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:100%', 'placeholder':'ZIP'}), required=True)