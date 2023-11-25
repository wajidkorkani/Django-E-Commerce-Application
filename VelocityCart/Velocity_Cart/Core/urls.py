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
    path('remove_from_cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/<int:pk>/', checkout, name='checkout'),
    path('buy-now/', buy_now, name='buy_now'),
    path('product-comment/<int:pk>/', Product_Comments, name='product_comment'),
    path('comment-reply/<int:pk>/', Comments_Replys, name='comments_replys'),
    path('comment-reply-page/<int:pk>/', Comments_Replys_Page, name='comments_replys_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
