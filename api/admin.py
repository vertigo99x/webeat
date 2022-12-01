from django.contrib import admin

# Register your models here.
from .models import Allusers, FoodItems, Reviews, Orders, Vendor, Events

stuff = [Allusers, FoodItems, Reviews, Orders, Vendor, Events]

for i in stuff:
    admin.site.register(i)