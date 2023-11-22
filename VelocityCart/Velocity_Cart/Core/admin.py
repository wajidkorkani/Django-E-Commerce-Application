from django.contrib import admin
from .models import Product, Categorey, CartItem, PurchaseProduct
# Register your models here.

admin.site.register(Product)
admin.site.register(Categorey)
admin.site.register(CartItem)
admin.site.register(PurchaseProduct)
