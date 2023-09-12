from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from config import settings

from . import views

app_name = "user"

urlpatterns = [
    path("registration", views.register, name="registration"),
    path("login", views.loginUser, name="login"),
    path("logout", LogoutView.as_view(
        next_page=settings.LOGOUT_REDIRECT_URL), name="logout"),
    path(
        "cart",
        views.cart,
        name="cart",
    ),
    path(
        "addToCart/<int:productPk>",
        views.addToCart,
        name="addToCart",
    ),
    path(
        "increaseQuantity/<int:cartItemPk>",
        views.increaseQuantity,
        name="increaseQuantity",
    ),
    path(
        "decreaseQuantity/<int:cartItemPk>",
        views.decreaseQuantity,
        name="decreaseQuantity",
    ),
    path(
        "removeFromCart/<int:cartItemPk>",
        views.removeFromCart,
        name="removeFromCart",
    ),
]
