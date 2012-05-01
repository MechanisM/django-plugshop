import time
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.conf import settings

class CartItem(object):
    def __init__(self, product, price=0, quantity=1):
        self.product = product
        self.price = price
        self.quantity = quantity

    def price_total(self):
        return self.price * self.quantity

class Cart(list):
    def __init__(self, request, name='plugshop.cart'):
        super(Cart, self).__init__()
        self.request = request
        self.name = name

        for item, quantity in request.session.get(self.name, []):
            self.append(item, quantity)
            
    def _get_product(self, product):
        try:
            return filter(lambda x: x.product.pk == product.pk, self)[0]
        except IndexError:
            return None

    def save(self):
        self.request.session[self.name] = tuple((item.product, item.quantity,) for item in self)
    
    def append(self, product, price=0, quantity=1):
        item = self._get_product(product)
        if item:
            self[self.index(item)].quantity += quantity
        else:
            super(Cart, self).append(
                CartItem(product, price, quantity)
            )

    def remove(self, product, quantity=None):
        item = self._get_product(product)
        if item:
            if quantity:
                if item.quantity > quantity:
                    self[self.index(item)].quantity -= quantity
                else:
                    super(Cart, self).remove(item)
            else:
                super(Cart, self).remove(item)
        
    def empty(self):
        while len(self):
            self.pop()

    def price_total(self):
        return sum([p.price_total() for p in self])

    def get_products(self):
        return [{'product': p.product.pk, 'quantity': p.quantity} for p in self]


class CartMiddleware(object):

    def process_request(self, request):
        request.cart = Cart(request)

    def process_response(self, request, response):
       if hasattr(request, 'cart'):
           request.cart.save()
       return response