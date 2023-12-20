from django.urls import path
from Auth.views import *
# from django.contrib.auth.views import PasswordResetCompleteView

urlpatterns = [

    path('registration-form/', Registration, name='signup'),

    path('otp/', verify_otp, name='verify_otp'),

    path('logout/', logout_user, name='logout_user'),


    # Password reset section
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),

    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('accounts/login/', login_view, name='login'),

]
