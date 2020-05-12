import datetime
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from user_app.models import SiteUser

class Category(models.Model):
    name = models.CharField(max_length=90,unique=True)
    category_discount = models.FloatField()

    def __str__(self):
        return self.name

class Product_model(models.Model):   #cleaned
    name = models.CharField(max_length=90)
    slug = models.SlugField(max_length=90,unique=True)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='product_iamges/')
    selling_cost = models.FloatField()
    selling_unit = models.CharField(max_length=13)
    rule_out_cost = models.CharField(max_length=20)
    tags = models.CharField(max_length=120)
    offer = models.BooleanField('Sale',default=False)
    ratings = models.FloatField(default=0.0)
    popularity = models.BigIntegerField(default=0)
    stock_quantity = models.BigIntegerField(default=0)
    entry_timedate = models.DateTimeField(default=timezone.now,)
