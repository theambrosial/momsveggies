from django.contrib import admin

from .models import Orders_rzp, Order_placed, payment_rzp
admin.site.register(Orders_rzp)
admin.site.register(Order_placed)
admin.site.register(payment_rzp)
