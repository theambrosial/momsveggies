
from django.contrib import admin
from django.urls import path, include
from .views import home, product_detail, account, delete_cart_item, delete_item, about_us, lost_password, logout_user

urlpatterns = [
    path('home/',home ,name='home'),
    # path('about/', about, name='about'),
    # path('cart/', contact, name='contact'),
    path('product_detail/', product_detail, name='product_detail'),
    path('account/', account, name='account'),
    path('delete_cart_item/', delete_cart_item, name='delete_cart_item'),
    path('delete_item/', delete_item, name='delete_item'),
    path('about_us/', about_us, name='about_us'),
    path('logout/', logout_user, name='logout'),
    path('lost_password/', lost_password, name='lost_password'),
]
