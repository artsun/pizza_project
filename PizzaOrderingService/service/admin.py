from django.utils import timezone
from django.contrib import admin

from .models import Status, Customer, Order, Product


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('summary', 'status', 'total_passed', 'updated_passed')
    list_filter = ('status',)
    ordering = ('created',)
    search_fields = ('customer__email',)
    summary = lambda self, obj: str(obj)
    summary.short_description = 'Order'
    total_passed = lambda self, obj: timezone.now() - obj.created
    total_passed.short_description = 'Total passed'
    updated_passed = lambda self, obj: timezone.now() - obj.status_updated
    updated_passed.short_description = 'Since last update'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
