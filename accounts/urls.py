from django.urls import path
from .views import register, user_login, user_logout, profile, customer_list

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('customers/', customer_list, name='customer_list'),
]