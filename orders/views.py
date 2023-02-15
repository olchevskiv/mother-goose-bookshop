from django.shortcuts import render
from django.http.response import JsonResponse

from cart.cart import Cart

from .models import Order, OrderItem

def add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        cust_name = request.POST.get('cust_name')
        cust_add = request.POST.get('cust_add')
        cust_add2 = request.POST.get('cust_add2')
        cust_zip_code = request.POST.get('cust_zip_code')
        user_id = request.user.id
        cart_total = cart.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name=cust_name, address1=cust_add,
                                address2=cust_add2, zip_code=cust_zip_code, total_paid=cart_total, order_key=order_key)
            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': True})
        return response

def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)

def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders