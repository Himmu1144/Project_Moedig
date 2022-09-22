from django.contrib import admin
from . models import Contact, Newsletter, Profile, Product, Order , Coupon , Employee

# Register your models here.
admin.site.register((Contact,Newsletter,Profile,Product,Order,Coupon,Employee))
