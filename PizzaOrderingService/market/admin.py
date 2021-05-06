from django.contrib import admin
from .models import Pizza, PizzaFlavor, Size


@admin.register(PizzaFlavor)
class PizzaFlavorAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('flavor', 'size')
    ordering = ('flavor',)
