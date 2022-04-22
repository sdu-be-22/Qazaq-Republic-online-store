from django.contrib import admin
from .models import *

admin.site.register(Order)
admin.site.register(Favors)
admin.site.register(Customer)
admin.site.register(ShippingAddress)
admin.site.register(Color)
admin.site.register(Size)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price',
                    'available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name', 'category')}


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_attr', 'quantity', 'date_added']
    list_editable = ['product_attr', 'quantity']


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product', 'color']
