from django.urls import path
from Core.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Home, name='home'),
    path('about-product/<int:product_id>/', Product_About_Page, name='Product_About_Page'),
    path('searchbar/', Searchbar, name='searchbar'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('increase_quantity/<int:pk>/', increase_quantity, name='increase_quantity'),
    path('remove_from_cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/<int:pk>/', checkout, name='checkout'),
    path('buy-now/', buy_now, name='buy_now'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
