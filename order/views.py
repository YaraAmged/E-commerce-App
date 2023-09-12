from django.shortcuts import redirect, render

from order.models import Order, OrderItem
from product.views import getUserCartItemsCount
from user.models import Cart, CartItem


def create(request):

    customer = request.user
    cart = Cart.objects.get(customer=customer)
    order = Order.objects.create(
        customerId=customer, totalPrice=cart.getTotal())
    cartItems = CartItem.objects.filter(cart=cart)
    for cartItem in cartItems:
        product = cartItem.product
        product.stockQuantity -= cartItem.quantity
        product.save()
        orderItem = OrderItem.objects.create(productId=product, quantity=cartItem.quantity,
                                             orderId=order, unitPrice=product.unitPrice)
        orderItem.save()
    order.save()
    cartItems.delete()
    return redirect("order:list")


def orders_list(request):
    status = request.GET.get("status")
    orders = Order.objects.filter(customerId=request.user)
    if status is not None and len(status) > 0:
        orders = orders.filter(status=status)
    return render(request, "orders.html", {"orders": orders, "cartCount": getUserCartItemsCount(request.user)})


def orders_details(request, orderPk):
    order = Order.objects.get(pk=orderPk)
    order.items = OrderItem.objects.filter(orderId=order)
    return render(request, "order-details.html", {"order": order, "cartCount": getUserCartItemsCount(request.user)})
