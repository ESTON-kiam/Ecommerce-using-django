from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'total_price')
    fields = ('product', 'quantity', 'price', 'total_price')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('id', 'user__username', 'user__email', 'shipping_address')
    readonly_fields = ('user', 'created_at', 'updated_at', 'total_price')
    fieldsets = (
        (None, {
            'fields': ('user', 'status', 'total_price')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address',)
        }),
        ('Payment Information', {
            'fields': ('payment_method',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [OrderItemInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('payment_method',)
        return self.readonly_fields


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total_price')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('order', 'product', 'quantity', 'price', 'total_price')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False