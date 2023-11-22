from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categorey(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    image1 = models.ImageField(upload_to='media/', blank=True)
    image2 = models.ImageField(upload_to='media/', blank=True)
    image3 = models.ImageField(upload_to='media/', blank=True)
    image4 = models.ImageField(upload_to='media/', blank=True)
    image5 = models.ImageField(upload_to='media/', blank=True)
    image6 = models.ImageField(upload_to='media/', blank=True)
    image7 = models.ImageField(upload_to='media/', blank=True)
    image8 = models.ImageField(upload_to='media/', blank=True)
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    categorey = models.ForeignKey(Categorey, on_delete=models.CASCADE)
    price = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CartItem(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product

class PurchaseProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=30)
    buyer_phone = models.CharField(max_length=30)
    buyer_email = models.CharField(max_length=30)
    buyer_address = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.buyer_name
