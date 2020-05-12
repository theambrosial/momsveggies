from django.db import models
from django.utils import timezone
from cart_app.models import Cart_model


class orders_rzp(models.Model):
    receipt = models.CharField(max_length=20)
    amount = models.CharField(max_length=20)
    razorpay_order_id = models.CharField(max_length=50)
    razorpay_payment_id = models.CharField(max_length=50)
    razorpay_signature = models.CharField(max_length=50)
    generated_signature = models.CharField(max_length=50)
    signature_matching_status = models.BooleanField()
    is_payment_successful = models.BooleanField()
    entry_timedate = models.DateTimeField(default=timezone.now, )


class Order_placed(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=40)
    city = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=6)
    address1 = models.CharField(max_length=90)
    address2 = models.CharField(max_length=90)
    country = models.CharField(max_length=20)
    payment_status = models.BooleanField(default=False)
    order_rzp_id = models.ForeignKey(orders_rzp, on_delete=models.DO_NOTHING)
    delivery_status = models.CharField(max_length=20,choices=(
        ('Preparing Order','Preparing Order'),
        ('Packing','Packing'),
        ('On the way','On the way'),
        ('Delivered','Delivered'),
    ))
    delivery_done = models.BooleanField(default=False)
    entry_timedate = models.DateTimeField(default=timezone.now, )

class payment_rzp(models.Model):
    amount = models.CharField(max_length=30)
    order_rzp_id = models.ForeignKey(orders_rzp, on_delete=models.DO_NOTHING)
    order_placed_id = models.ForeignKey(Order_placed, on_delete=models.DO_NOTHING)
    cart_model_id = models.ForeignKey(Cart_model, on_delete=models.DO_NOTHING)
    razorpay_payment_id = models.CharField(max_length=50)
    entry_timedate = models.DateTimeField(default=timezone.now, )


