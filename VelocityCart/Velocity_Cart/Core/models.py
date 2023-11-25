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
    description = models.TextField()
    categorey = models.ForeignKey(Categorey, on_delete=models.CASCADE)
    price = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CartItem(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    time_stamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product

class PurchaseProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product_id_number = models.CharField(max_length=100000, null=True)
    registration_email = models.EmailField(null=True)
    quantity = models.IntegerField(default=1)
    color = models.CharField(max_length=20, null=True)
    buyer_name = models.CharField(max_length=30)
    buyer_phone = models.CharField(max_length=30)
    buyer_email = models.EmailField()
    buyer_address = models.CharField(max_length=100, null=True)
    time_stamp = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.buyer_name} - {self.product.title}"

class ProductComments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=1000)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class CommentReply(models.Model):
    comment = models.ForeignKey(ProductComments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reply = models.CharField(max_length=1000)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class HomePageImage(models.Model):
    image = models.ImageField(upload_to='media/', blank=True)
