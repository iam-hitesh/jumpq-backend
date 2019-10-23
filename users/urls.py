from django.urls import re_path

from .views import *

urlpatterns = [
    re_path('^merchant-login/$', MerchantLogin.as_view(), name="merchant-login"),
    re_path('^login/$', CustomerLogin.as_view(), name="customer-login"),
    re_path('^send-otp/$', SendOTP.as_view(), name="send-otp")
]
