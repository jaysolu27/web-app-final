from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CategoryModel(models.Model):
    c_name = models.CharField(max_length=40, unique=True)
    c_desc = models.TextField(default=None)
    def __str__(self) -> str:
        return self.c_name

class BrandModel(models.Model):
    b_name = models.CharField(max_length=50, unique=True)
    b_desc = models.TextField(default=None)

    def __str__(self) -> str:
        return self.b_name

from datetime import datetime
from django.utils import timezone
import pytz

class ProductModel(models.Model):
    p_name = models.CharField(max_length=256, unique=True)
    p_desc = models.TextField()
    p_category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    p_brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    p_img = models.ImageField(upload_to='media')
    p_price = models.FloatField()
    
    def __str__(self) -> str:
        return self.p_name
    

class UserCart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    product_count = models.IntegerField()


class ReviewModel(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    review = models.TextField()

class OrderDetailsModel(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    product_count = models.IntegerField()
    ft_name = models.CharField(max_length=200, null=True, default=None)
    lt_name = models.CharField(max_length=200,null=True, default=None)
    country = models.CharField(max_length=200,null=True, default=None)
    address = models.TextField(null=True, default=None)
    town = models.CharField(max_length=200,null=True, default=None)
    state = models.CharField(max_length=200,null=True, default=None)
    zip = models.CharField(max_length=200,null=True, default=None)
    phone = models.CharField(max_length=200,null=True, default=None)
    email = models.CharField(max_length=200,null=True, default=None)
    date_time = models.DateTimeField(default=timezone.now)





