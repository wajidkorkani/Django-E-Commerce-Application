from django import forms
from Core.models import PurchaseProduct, ProductComments

class BuyForm(forms.ModelForm):
    class Meta:
        model = PurchaseProduct
        fields = ['buyer_phone', 'buyer_email', 'buyer_address', 'quantity', 'color']


class CommenForm(forms.ModelForm):
    class Meta:
        model = ProductComments
        fields = ['comment']
