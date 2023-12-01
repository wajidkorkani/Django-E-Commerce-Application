from django.urls import path
from Auth.views import *

urlpatterns = [

    path('registration-form/', Registration, name='signup'),

    path('otp/', verify_otp, name='verify_otp'),

    path('login/', login_view, name='login'),
    
    path('logout/', logout_user, name='logout_user')
]
