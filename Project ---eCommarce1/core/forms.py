from django import forms
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator
from django_countries.widgets import CountrySelectWidget
from .models import BillingAddress, Coupon, Refund

PAYMENT_CHOICES = (
    ('C',"Credit Card"),
    ('M',"Master Card"),
    ('P','Paypal'),
    ('Py','Payoneer'),
    
)
class CheckoutForm(forms.ModelForm):
    address = forms.CharField(max_length=300, widget=forms.TextInput(attrs={
        'placeholder':'1234 Main St','class':'form-control'
    }))
    apartment_address = forms.CharField(max_length = 200, required=False,
                             widget=forms.TextInput(attrs={
                            'placeholder':'Apartment or suite',
                            'class':'form-control' }))
    country = CountryField(blank_label='(select country)').formfield(
                        required=True,widget=CountrySelectWidget(attrs={
                                    'class': 'custom-select d-block w-100',
        }))
    zipcode = forms.CharField(required=False,widget=forms.TextInput(attrs={
                            'class':'form-control' }))
    same_billing_address = forms.BooleanField(widget=(forms.CheckboxInput()))
    save_info = forms.BooleanField(widget=(forms.CheckboxInput()))
    
    payment_method = forms.ChoiceField(widget=forms.RadioSelect,
                        choices=PAYMENT_CHOICES)

    class Meta:
        model = BillingAddress
        fields = ['address', 'apartment_address', 'country', 'zipcode', 'same_billing_address', 'save_info', 'payment_method']


class CouponForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))
    class Meta:
        model = Coupon
        fields = ['code']
    
class RefundForm(forms.ModelForm):
    code = forms.CharField(max_length=50)
    
    class Meta:
        model = Refund
        fields = ['code','reason']