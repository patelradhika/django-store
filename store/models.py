from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="user_profile", default="user_profile/default_pic.png")
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return self.device

class Products(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=400, null=True, blank=True)
    product_pic = models.ImageField(upload_to="products", default="products/no_image.png")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField(default=False)
    dateAdded = models.DateTimeField(auto_now_add=True)
    transactionId = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'Order: {str(self.id)} Complete: {self.complete} TransID: {str(self.transactionId)}'

    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total

    @property
    def get_cart_items(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total

    @property
    def get_items(self):
        return self.orderitem_set.all()



class OrderItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order ID: {str(self.order.id)} -- Product: {self.product.name}"

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    firstName = models.CharField(max_length=200, null=False)
    lastName = models.CharField(max_length=200, null=False)
    addressLine1 = models.CharField(max_length=200, null=False)
    addressLine2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.addressLine1

    class Meta:
        verbose_name_plural = 'Shipping Addresses'