
from django.contrib import admin
from django.urls import path, include
from .views import home, product_detail, account

urlpatterns = [
    path('home/',home ,name='home'),
    # path('about/', about, name='about'),
    # path('cart/', contact, name='contact'),
    path('product_detail/', product_detail, name='product_detail'),
    path('account/', account, name='account'),
]
