from django.contrib import admin
from .models import Order, Product,Categories,Variant,OrderItem,ShippingAddress,OrderUpdates
# Register your models here.

admin.site.register((Categories,Variant,Order,OrderItem,ShippingAddress,OrderUpdates))

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Media:
        js=('TI.js',)

