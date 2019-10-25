from django.urls import re_path

from .views import *

urlpatterns = [
    re_path('^login/$', LoginView.as_view(), name="user-login"),
    re_path('^send-otp/$', SendOTP.as_view(), name="send-otp"),
    re_path('^country/$', CountryView.as_view(), name='country'),
    re_path('^state/$', StateView.as_view(), name='state')
]
