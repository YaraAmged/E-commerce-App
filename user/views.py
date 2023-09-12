from multiprocessing import AuthenticationError
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate


from user.forms import LoginForm, RegisterForm, RegisterForm_Customer_profile

from .models import Cart, CartItem, CustomerProfile

# Create your views here.


def register(request):
    print(request.method)
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        register_from_customer_profile = RegisterForm_Customer_profile(
            request.POST)
        if register_form.is_valid() and register_from_customer_profile.is_valid():
            print(register_form)
            user = register_form.save()
            user.set_password(user.password)
            user.customerProfile = CustomerProfile.objects.create(
                user=user, phone=register_from_customer_profile.data["phone"],
                address=register_from_customer_profile.data["address"])
            user.save()
            Cart.objects.create(customer=user).save()
            login(request, user)
            return redirect("product:list")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Invalid email or password")

    register_form = RegisterForm()
    register_from_customer_profile = RegisterForm_Customer_profile()
    return render(request, "registration.html", {"register_form": register_form, "register_from_customer_profile": register_from_customer_profile})


def loginUser(request):
    if request.method == "POST":
        try:
            login_form = LoginForm(request.POST)
            if login_form.is_valid() is False:
                raise AuthenticationError
            print(login_form.data["email"])
            user = authenticate(
                email=login_form.data["email"], password=login_form.data["password"])
            if user is None:
                print("NO user")
                raise AuthenticationError
            login(request, user)
            return redirect("product:list")
        except:

            messages.add_message(request, messages.ERROR,
                                 "Invalid email or password")
            print("Invalid email or password")

    return render(request, "login.html", {"login_form": LoginForm()})


def cart(request):
    cart = Cart.objects.get(customer=request.user)
    cartItems = CartItem.objects.filter(cart_id=cart.pk)
    context = {"cartItems": cartItems, "cartCount": len(
        cartItems), "cartTotal": cart.getTotal()}

    return render(request, "cart.html", context)


def addToCart(request, productPk):
    cart = Cart.objects.get(customer=request.user)
    cart.addToCart(productPk, 1)
    return redirectToSourceOrCart(request)


def increaseQuantity(request, cartItemPk):
    cart = Cart.objects.get(customer=request.user)
    cart.updateCartItem(cartItemPk, 1)
    return redirectToSourceOrCart(request)


def decreaseQuantity(request, cartItemPk):
    cart = Cart.objects.get(customer=request.user)
    cart.updateCartItem(cartItemPk, -1)
    return redirectToSourceOrCart(request)


def removeFromCart(request, cartItemPk, ):
    cart = Cart.objects.get(customer=request.user)
    cart.removeFromCart(cartItemPk)
    return redirectToSourceOrCart(request)


def logoutUser(request):
    logout(request)
    return redirect(request, "product:list")


def redirectToSourceOrCart(request):
    source = request.GET.get("source")
    if source is None:
        source = "user:cart"
    return redirect(source)
