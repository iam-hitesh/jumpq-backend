from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^api/v1/', include('users.urls'), name="users"),
    re_path('^api/v1/stores/', include('merchants.urls'), name="merchants"),
]