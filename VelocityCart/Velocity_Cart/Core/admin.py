from django.contrib import admin
from .models import Product, Categorey, CartItem, PurchaseProduct, HomePageImage, ProductComments, CommentReply
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductComments)
admin.site.register(CommentReply)
admin.site.register(Categorey)
admin.site.register(CartItem)
admin.site.register(PurchaseProduct)
admin.site.register(HomePageImage)
