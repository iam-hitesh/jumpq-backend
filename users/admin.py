from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Addresses)
# admin.site.register(FareMap)
# admin.site.register(Packages)
# admin.site.register(Trips)
# admin.site.register(PaymentDetails)