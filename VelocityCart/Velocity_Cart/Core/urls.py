from django.urls import path
from Core.views import *

urlpatterns = [
    path('', Home, name='login'),
]
