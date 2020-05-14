from django.urls import path, include
from .views import checkout,payment,payment_confirmation

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('payment', payment, name='make-payment'),
    path('payment-confirmation/<str:orders_rzp>/<str:orders>', payment_confirmation, name='payment_confirmation'),

]
