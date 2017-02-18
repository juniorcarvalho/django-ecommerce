from django.contrib import admin
from .models import Product, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created', 'modified']
    search_fields = ['name']
    list_filter = ['created', 'modified']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','category', 'price', 'created', 'modified']
    search_fields = ['name', 'category__name']
    list_filter = ['created', 'modified']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

