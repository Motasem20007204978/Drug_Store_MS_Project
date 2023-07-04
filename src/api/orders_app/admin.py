from django.contrib import admin

from .models import Order, OrderedDrug

admin.site.register(Order)
admin.site.register(OrderedDrug)
