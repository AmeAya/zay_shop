from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager

ORDER_STATUSES = [(currency, currency) for currency in ['Accepted', 'Declined', 'In Delivery', 'Received']]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    favourites = models.ManyToManyField('Product')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class Gender(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'Genders'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    thumb = models.ImageField(upload_to='categories')
    popular = models.BooleanField(default=False)
    gender = models.ForeignKey('gender', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    thumb = models.ImageField(upload_to='brands', null=True, blank=True)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    thumb = models.ImageField(upload_to='thumbs/')
    images = models.ManyToManyField('ProductImage')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    order_counter = models.PositiveIntegerField(default=0)
    popular = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    total = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.product} {self.quantity}"


class Order(models.Model):
    customer = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    items = models.ManyToManyField('OrderItem')
    total = models.PositiveBigIntegerField()
    datetime = models.DateTimeField(default=timezone.now())
    status = models.CharField(max_length=100, choices=ORDER_STATUSES)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"{self.customer} {self.datetime}"
