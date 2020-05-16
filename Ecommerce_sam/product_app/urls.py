
from django.urls import path, include
from .views import all_products, product_detail, load_category,add_to_cart_ajax, load_search_res

urlpatterns = [
    path('', all_products, name='all_products'),
    path('load_category/', load_category, name='load_category'),
    path('load_search_res/', load_search_res, name='load_search_res'),
    path('add_to_cart_ajax/', add_to_cart_ajax, name='add_to_cart_ajax'),
    path('product_detail/<str:slug>', product_detail, name='product_detail'),
]
