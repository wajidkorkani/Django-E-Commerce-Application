from django.urls import path
from Auth.views import *

urlpatterns = [
    path('login/', login, name='login'),
]
