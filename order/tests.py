from django.urls import reverse
from django.test import Client, TestCase
from order.models import Order, OrderItem
from product.models import Category, Product

from user.models import Cart, CartItem, User

# Create your tests here.


class orderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='testuser@email.com',
            password='testpassword'
        )
        self.user.set_password("testpassword")
        self.user.save()
        self.cart = Cart.objects.create(customer=self.user)
        self.category = Category.objects.create(name="Bags")
        self.product = Product.objects.create(
            nameEn="test", nameAr="test", unitPrice=12, categoryId=self.category, stockQuantity=10)
        self.product2 = Product.objects.create(
            nameEn="test", nameAr="test", unitPrice=12, categoryId=self.category, stockQuantity=10)
        self.client = Client()
        self.client.login(
            email='testuser@email.com', password='testpassword')

    def test_create_order(self):
        CartItem.objects.create(
            cart=self.cart, quantity=1, product=self.product)
        CartItem.objects.create(
            cart=self.cart, quantity=1, product=self.product2)
        response = self.client.post(reverse('order:create'), {})
        self.assertEqual(response.url, "/orders/")
        self.assertEqual(response.status_code, 302)
        orders = Order.objects.filter(customerId=self.user)
        self.assertEqual(len(orders), 1)
        self.assertEqual(
            len(OrderItem.objects.filter(orderId=orders.first())), 2)
