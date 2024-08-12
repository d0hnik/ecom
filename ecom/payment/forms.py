from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(
        label='Täisnimi',
        widget=forms.TextInput(
            attrs={'class': "form-control", 'id': 'FullName', 'placeholder': ' '}
        ),
        required=True
    )
    shipping_email = forms.CharField(
        label='E-posti aadress',
        widget=forms.EmailInput(
            attrs={'class': "form-control", 'id': 'Email', 'placeholder': ' '}
        ),
        required=True
    )
    shipping_address1 = forms.CharField(
        label='Aadress',
        widget=forms.TextInput(
            attrs={'class': "form-control", 'id': 'Aadress', 'placeholder': ' '}
        ),
        required=True
    )
    shipping_address2 = forms.CharField(
        label='Aadress 2',
        widget=forms.TextInput(
            attrs={'class': "form-control", 'id': 'Aadress2', 'placeholder': ' '}
        ),
        required=False
    )
    shipping_city = forms.CharField(
        label='Linn',
        widget=forms.TextInput(
            attrs={'class': "form-control", 'id': 'City', 'placeholder': ' '}
        ),
        required=True
    )
    shipping_state = forms.CharField(
        label='Vald',
        widget=forms.TextInput(
            attrs={'class': "form-control", 'id': 'State', 'placeholder': ' '}
        ),
        required=False
    )
    shipping_zipcode = forms.CharField(
        label='Posti indeks',
        widget=forms.TextInput(
            attrs={'class': "form-control", 'id': 'ZipCode', 'placeholder': ' '}
        ),
        required=False
    )
    shipping_country = forms.CharField(
        label='Riik',
        widget=forms.TextInput(
            attrs={'class': "form-control", 'id': 'Country', 'placeholder': ' '}
        ),
        required=True
    )

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city',
                  'shipping_state', 'shipping_zipcode', 'shipping_country']
        exclude = ['user', ]


class PaymentForm(forms.Form):
    card_name = forms.CharField(
        label='Nimi kaardil',
        widget=forms.TextInput(attrs={
            'class': 'payment-input',
            'placeholder': 'Nimi'
        }),
        required=True
    )
    card_number = forms.CharField(
        label='Kaardi Number',
        widget=forms.TextInput(attrs={
            'id': 'ccn',
            'type': 'tel',
            'class': 'payment-input',
            'inputmode': 'numeric',
            'pattern': '[0-9\s]{13,19}',
            'autocomplete': 'cc-number',
            'maxlength': '19',
            'placeholder': 'XXXX XXXX XXXX XXXX'
        }),
        required=True
    )
    card_cvv = forms.CharField(
        label='CVV',
        widget=forms.TextInput(attrs={
            'class': 'payment-input-small',
            'placeholder': '***',
            'type': 'text'
        }),
        required=True
    )
    card_exp_date = forms.CharField(
        label='Expiration Date',
        widget=forms.TextInput(attrs={
            'class': 'payment-input-small',
            'placeholder': 'MM/YYYY',
            'inputmode': 'numeric',
            'autocompletetype': 'cc-exp'
        }),
        required=True
    )
