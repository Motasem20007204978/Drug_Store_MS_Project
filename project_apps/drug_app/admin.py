from django.contrib import admin
from .models import Drug

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'quantity',
        'exp_date',
        'drug_price',
        'availability',
    )
    list_filter = ('exp_date', 'availability')
    search_fields = ('name',)
    date_hierarchy = 'created_at'
