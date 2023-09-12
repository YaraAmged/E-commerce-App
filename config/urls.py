from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("product.urls", namespace="product")),
    path("user/", include("user.urls", namespace="user")),
    path("orders/", include("order.urls", namespace="order")),
]
