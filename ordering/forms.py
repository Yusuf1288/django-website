from django import forms
from ordering.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'country', 'district', 'region']

    def __init__(self,*args,**kwargs):
        super(OrderForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['address'].widget.attrs['placeholder'] = 'Enter Address'
        self.fields['country'].widget.attrs['placeholder'] = 'Enter Country'
        self.fields['district'].widget.attrs['placeholder'] = 'Enter District'
        self.fields['region'].widget.attrs['placeholder'] = 'Enter Region'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

