from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock', 'available']
    list_filter = ['available', 'category', 'created_at']
    list_editable = ['price', 'discount_price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
