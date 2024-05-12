from django.contrib import admin
from .models import *


admin.site.register([CustomUser, Gender, Category, Brand, Product, ProductImage, OrderItem, Order])
