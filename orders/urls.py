from django.urls import path
from .views import (
    create_order, order_detail, order_list,
    admin_order_list, admin_order_detail, update_order_status,
)

urlpatterns = [
    path('checkout/', create_order, name='checkout'),
    path('my-orders/', order_list, name='order_list'),
    path('my-orders/<int:order_id>/', order_detail, name='order_detail'),
    path('admin/orders/', admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
    path('admin/orders/<int:order_id>/update-status/', update_order_status, name='update_order_status'),
]