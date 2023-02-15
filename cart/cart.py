from store.models import Product
from decimal import Decimal
from django.conf import settings

class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in self.session:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, qty):
        product_id = str(product.id)

        if (product_id not in self.cart):
            self.cart[product_id] = {'price':str(product.price), 'qty':qty}
        else:
            self.cart[product_id]['qty'] = qty

        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product_id, qty):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
            self.save()
            return  (Decimal(self.cart[product_id]['price']) * self.cart[product_id]['qty'])

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.products.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def get_total_price(self):
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(11.50)

        total = subtotal + Decimal(shipping)
        return total

    def clear(self):
        # Remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True