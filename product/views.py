import functools
from urllib import request
from django.shortcuts import render

from product.models import Category, Product
from user.models import Cart, CartItem, User

app_name = "product"


def getQueryParameterIfDefined(request, key):
    value = request.GET.get(key)
    if value is not None and len(value) > 0:
        return value
# Create your views here.


def product_list(request):

    # view all products
    products = Product.objects.all()

    # filter products by Category
    category = getQueryParameterIfDefined(request, "category")
    if category:
        products = products.filter(categoryId__name=category)

    # filter products by price range
    min_price = getQueryParameterIfDefined(request, "min_price")
    if min_price:
        products = products.filter(
            unitPrice__gte=(int(min_price)))
    max_price = getQueryParameterIfDefined(request, 'max_price')
    if max_price:
        products = products.filter(
            unitPrice__lte=(int(max_price)))

    # filter products by search name
    searchKeyword = getQueryParameterIfDefined(request, 'searchKeyword')
    if searchKeyword:
        products = products.filter(nameEn__icontains=searchKeyword.strip())

    user = getUserFromRequest(request)
    cartItems = getUserCartItems(user)
    for product in products:
        for cartItem in cartItems:
            if product.pk == cartItem.product.pk:
                product.cartItem = cartItem
    context = {"cartCount": getUserCartItemsCount(
        user), "products": products, "categories": Category.objects.all()}
    return render(request, "products.html", context)


def getUserFromRequest(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        print("user", user)
        return user


def getUserCartItemsCount(user):
    if user is None:
        return 0
    cart = Cart.objects.get(customer=user)
    return len(CartItem.objects.filter(cart=cart))


def getUserCartItems(user):
    if user is None:
        return list()
    cart = Cart.objects.get(customer=user)
    return CartItem.objects.filter(cart=cart)
