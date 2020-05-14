import datetime
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from user_app.models import SiteUser
from product_app.models import Product_model

class Cart_model(models.Model):
    total_cost = models.FloatField()
    total_quantity = models.BigIntegerField()
    user_id = models.ForeignKey(SiteUser,models.DO_NOTHING,null=True,blank=True)
    session_id = models.CharField(max_length=90,unique=True,null=True,blank=True)
    is_payment_done = models.BooleanField(default=False)
    entry_timedate = models.DateTimeField(default=timezone.now,)


class Cart_products(models.Model):
    cart_id = models.ForeignKey(Cart_model,on_delete=models.CASCADE)
    product = models.ForeignKey(Product_model,on_delete=models.CASCADE)
    product_quantity = models.BigIntegerField()
    product_cost = models.FloatField()
    entry_timedate = models.DateTimeField(default=timezone.now,)