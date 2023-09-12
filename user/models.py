import functools
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver

from product.models import Product

from .managers import UserManager


class User(AbstractUser):
    username = None
    fullName = models.CharField(max_length=200)
    email = models.EmailField(
        max_length=200,
        unique=True,
    )

    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    def __str__(self): return self.fullName


class AdminProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="adminProfile"
    )
    jobTitle = models.CharField(max_length=200)
    hireDate = models.DateField()

    class Meta:
        verbose_name_plural = "Admin Profile"


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customerProfile"
    )
    phone = models.IntegerField()
    address = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Customer Profile"


@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            instance.adminProfile = AdminProfile.objects.create(
                user=instance, jobTitle="admin", hireDate="2021-05-05"
            )


@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_superuser:
        instance.adminProfile.save()


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def addToCart(self, productPk, quantity):
        CartItem.objects.create(
            product_id=productPk, quantity=quantity, cart_id=self.pk).save()

    def updateCartItem(self, cartItemPk, quantity):
        cartItem = CartItem.objects.get(pk=cartItemPk)
        cartItem.quantity += quantity
        cartItem.save()

    def removeFromCart(self, cartItemPk):
        cartItem = CartItem.objects.get(pk=cartItemPk)
        cartItem.delete()

    def getTotal(self):
        cartItems = CartItem.objects.filter(cart=self.pk)
        total = functools.reduce(
            lambda total, cartItem: total + cartItem.getSubtotal(), cartItems, 0
        )
        return total

    def __str__(self): return self.customer.fullName + " Cart "


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def getSubtotal(self):
        return self.quantity * self.product.unitPrice

    def __str__(self):
        return str(self.pk)
