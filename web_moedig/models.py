from itertools import chain
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import json , os
from django.utils.timezone import now

# Create your models here.

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default='')
    email = models.CharField(max_length=500,default='')
    phone = models.CharField(max_length=13,default='')
    message = models.TextField(max_length=10000,default='')
    date = models.DateTimeField(default=now)

    def __str__(self):
        return f'name - {self.name} | Message - {self.message[0:20]}...'

class Newsletter(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=500,default='')

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    # choice = (
    #     ('Order Placed','Order Placed'),
    #     ('Order Printed','Order Printed'),
    #     ('Order Shipped','Order Shipped'),
    #     ('Order Picked','Order Picked')
    # )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_json = models.CharField(max_length=20000)
    order_date = models.DateTimeField(default=now)
    # producti = models.ManyToManyField('Product', related_name='ordered_products')
    order_id = models.CharField(max_length=1000)
    bill = models.FloatField(null=False)
    tslot = models.CharField(max_length=50)
    pickup = models.CharField(max_length=1000)
    delivery = models.CharField(max_length=1000)
    phone = models.CharField(max_length=13)
    payment_status = models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=1000,default='Order Placed')
    
    # razorpay 
    payment_id = models.CharField(max_length=1000)

    def __str__(self):
        return f'Order Id : {self.order_id}'

    def load_json(self):
        return json.loads(self.product_json)
    


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True,)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    uploaded_file = models.FileField()
    items_json = models.CharField(max_length=10000,default='')
    price = models.CharField(max_length=10000)

    def __str__(self):
        return self.uploaded_file.name
    
    def loading_json(self):
        return json.loads(self.items_json)
    
    def fname(self):
        f_name = self.uploaded_file.name
        mf_name = os.path.splitext(f_name)[0]
        mf_ext = os.path.splitext(f_name)[1]
        return mf_name

class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    coupon = models.CharField(max_length=20)
    discount = models.IntegerField()

    def __str__(self):
        return self.coupon

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=2000)
    message = models.CharField(max_length=20000,blank=True,null=True)

    def __str__(self):
        return self.user.username + " | " + self.order_id
    

