from django.urls import path
from .views import (
    ProductListView, 
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),  # Moved up
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('<slug:slug>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),  # Moved to last
]