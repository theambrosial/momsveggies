
from django.urls import path, include
from .views import all_products, product_detail

urlpatterns = [
    path('', all_products, name='all_products'),
    path('product_detail/<str:slug>', product_detail, name='product_detail'),
]
