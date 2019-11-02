# from django.contrib import admin
# from django.contrib.gis.admin import OSMGeoAdmin
#
# from .models import *
# # Register your models here.
#
# @admin.register(MerchantStores)
# class ShopAdmin(OSMGeoAdmin):
#     list_display = ('store_location')

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from merchants import models


admin.site.register(models.MerchantCategory)
admin.site.register(models.Merchant)

@admin.register(models.Store)
class NearbyAdmin(OSMGeoAdmin):
    list_display = ('merchant', 'store_location')

