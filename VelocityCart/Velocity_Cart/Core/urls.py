from django.urls import path
from Core.views import *

urlpatterns = [
    path('', Home, name='home'),
    path('about-product/<int:product_id>/', Product_About_Page, name='Product_About_Page'),
    path('searchbar/', Searchbar, name='searchbar'),
]
