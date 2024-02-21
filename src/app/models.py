from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
import datetime
import os
import random
from PIL import Image
import uuid
# import barcode
# from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from django.core.validators import MinValueValidator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_file_path(instance, filename):
    new_filename = random.randint(1, 3231546414654785)
    name, ext =get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "item_images/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

def barcode_upload_file_path(instance, filename):
    new_filename = instance.uid
    name, ext =get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "barcodes/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class Address(models.Model):
    H = 1
    OF = 2
    OT = 0
    TYPE_CHOICES = (
        (OT, 'Other'),
        (H, 'Home'),
        (OF , 'Office'),
    )
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    line            = models.CharField(max_length=400)
    line_2          = models.CharField(max_length=15, null=True, blank=True)
    city            = models.CharField(max_length=30)
    pincode         = models.CharField(max_length=6)
    country         = models.CharField(max_length=100, default='India')
    type            = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, null=True, blank=True)

    latitude        = models.CharField(max_length=30)
    logitude        = models.CharField(max_length=30)

    is_active       = models.BooleanField(default=True)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.line


class Category(models.Model):
    parrent         = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    title           = models.CharField(max_length=150)
    added_by        = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    image           = models.ImageField(upload_to=upload_file_path)

    is_active       = models.BooleanField(default=True)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Item(models.Model):

    grams = 1
    kilograms = 2
    units = 3
    liter = 4
    ml = 5

    MES_CHOICES = (
        (grams, 'Grams'),
        (kilograms, 'Kilograms'),
        (units, 'Units'),
        (liter, 'Liter'),
        (ml, 'MiliLeter'),
    )

    title                   = models.CharField(max_length=100)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    category                = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    uid                     = models.CharField(max_length=20, help_text='ID must be unique')

    price                   = models.DecimalField(decimal_places=2, max_digits=20, default='00.00')
    type                    = models.PositiveSmallIntegerField(choices=MES_CHOICES, default=1, null=True, blank=True)
    capacity                = models.CharField(max_length=200, null=True, blank=True)

    barcode                 = models.ImageField(upload_to=barcode_upload_file_path, null=True, blank=True)
    stock                   = models.IntegerField(default=1, validators=[MinValueValidator(1),])

    is_active               = models.BooleanField(default=True)
    is_temprory             = models.BooleanField(default=False)
    created                 = models.DateTimeField(auto_now_add=True)
    updated                 = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    class Meta:
        unique_together = (('user', 'uid'),)
    
    # def save(self, *args, **kwargs):
    #     EAN = barcode.get_barcode_class('ean13')
    #     uid = random.randint(0000000000000,9999999999999)
    #     self.uid = uid
    #     ean = EAN(f'{uid}', writer=ImageWriter())
    #     buffer = BytesIO()
    #     ean.write(buffer)
    #     self.barcode.save('barcode.png', File(buffer), save=False)
    #     super().save(*args, **kwargs)


class OrderItem(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    buying_price = models.DecimalField(decimal_places=2, max_digits=20, default='00.00')

    def save(self, *args, **kwargs):
        self.buying_price = self.item.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return int(self.quantity) * self.buying_price


class Order(models.Model):

    placed = 1
    shipped = 2
    complete = 3
    canceled = 4

    STATUS_CHOICES = (
        (placed, 'Placed'),
        (shipped, 'Shipped'),
        (complete, 'Completed'),
        (canceled, 'Canceled/Refunded'),
    )

    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name       = models.CharField(max_length=200, blank=True, null=True)
    customer_mobile     = models.CharField(max_length=200, blank=True, null=True)
    items               = models.ManyToManyField(OrderItem)
    created             = models.DateTimeField(auto_now_add=True)
    ordered_date        = models.DateTimeField()
    shipping_address    = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    
    status              = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1, null=True, blank=True)
    received            = models.BooleanField(default=False)
    ordered             = models.BooleanField(default=False)
    is_payment_done     = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total


class Barcode(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    image        = models.ImageField(upload_to=upload_file_path)

    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username


class Message(models.Model):
    title = models.CharField(max_length=200)
    text  = models.TextField(max_length=1000)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pk',)