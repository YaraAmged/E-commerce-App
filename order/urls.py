from django.urls import path

from . import views

app_name = "order"
urlpatterns = [

    path("", views.orders_list, name="list"),
    path("create", views.create, name="create"),
    path("<int:orderPk>", views.orders_details, name="details"),
]
