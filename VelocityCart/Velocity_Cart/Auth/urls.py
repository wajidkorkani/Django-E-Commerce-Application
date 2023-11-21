from django.urls import path
from Auth.views import *

urlpatterns = [
    path('registration-form/', Registration, name='signup'),
    path('otp/', verify_otp, name='verify_otp'),
    path('login/', login, name='login'),
    path('logout/', login_user, name='login_user')
]
