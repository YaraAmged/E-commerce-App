from django.db import models

from product.models import Product
from user.models import User


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Declined", "Declined"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    ]
    createdAt = models.DateTimeField(auto_now_add=True)
    totalPrice = models.DecimalField(decimal_places=2, max_digits=10)
    customerId = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return str(self.pk)


class OrderItem(models.Model):
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    unitPrice = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.pk)
