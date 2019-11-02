from django.urls import re_path

from .views import *

urlpatterns = [
    re_path('^nearby/$', NearbyStores.as_view(), name="nearby-stores"),
]
