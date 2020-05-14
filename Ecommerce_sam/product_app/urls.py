
from django.urls import path, include
from .views import all_products, product_detail, load_category

urlpatterns = [
    path('', all_products, name='all_products'),
    path('load_category/', load_category, name='load_category'),
    path('product_detail/<str:slug>', product_detail, name='product_detail'),
]
