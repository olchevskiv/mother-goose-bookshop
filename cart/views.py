from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from store.models import Product
from .cart import Cart 

def cart_summary(request):
    return render(request, 'cart/summary.html')

def cart_add(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, qty=product_qty)
        return JsonResponse({'qty': cart.__len__()})

def cart_remove(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        cart.remove(product_id=(int(request.POST.get('productid'))))
        return JsonResponse({'qty': cart.__len__(), 'subtotal': (cart.get_subtotal_price())})

def cart_update(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        productid = int(request.POST.get('productid'))
        productqty = int(request.POST.get('productqty'))
        price = cart.update(product_id=productid, qty=productqty)
        return JsonResponse({'qty': cart.__len__(), 'totalprice': price, 'subtotal': (cart.get_subtotal_price())})
    