from operator import le
from django.test import Client, TestCase
from django.urls import reverse
from product.models import Category, Product

from user.models import Cart, CartItem, User


# Create your tests here.


class CartTestCase(TestCase):
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
        self.client = Client()
        self.client.login(
            email='testuser@email.com', password='testpassword')

    def test_cart_creation(self):
        self.assertEqual(self.cart.customer, self.user)

    def test_add_item_to_cart(self):
        url = reverse('user:addToCart', args=[self.product.pk])
        response = self.client.post(url, {'productPk': self.product.pk})
        self.assertEqual(response.url, "/user/cart")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(CartItem.objects.filter(cart=self.cart)), 1)

    def test_increase_cart_item_quantity(self):
        cartItem = CartItem.objects.create(
            cart=self.cart, quantity=1, product=self.product)
        response = self.client.put(
            reverse('user:increaseQuantity', args=[cartItem.pk]))
        self.assertEqual(response.url, "/user/cart")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.filter(
            cart=self.cart).first().quantity, 2)

    def test_decrease_cart_item_quantity(self):
        cartItem = CartItem.objects.create(
            cart=self.cart, quantity=2, product=self.product)
        response = self.client.put(
            reverse('user:decreaseQuantity', args=[cartItem.pk]))
        self.assertEqual(response.url, "/user/cart")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.filter(
            cart=self.cart).first().quantity, 1)

    def test_remove_cart_item(self):
        cartItem = CartItem.objects.create(
            cart=self.cart, quantity=2, product=self.product)
        response = self.client.put(
            reverse('user:removeFromCart', args=[cartItem.pk]))
        self.assertEqual(response.url, "/user/cart")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.filter(cart=self.cart).first(), None)
