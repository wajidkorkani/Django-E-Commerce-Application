from django import forms
from Core.models import PurchaseProduct

class BuyForm(forms.ModelForm):
    class Meta:
        model = PurchaseProduct
        fields = ['buyer_name', 'buyer_phone', 'buyer_email', 'buyer_address']
