from itertools import product

from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get IDS from cart
        product_ids = self.cart.keys()
        # Get actual products from db
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantities(self):
        quantities = self.cart
        return quantities

    def update(self, product_id, quantity):
        prod_id = str(product_id)
        product_qty = int(quantity)
        cart = self.cart
        cart[prod_id] = int(product_qty)
        self.session.modified = True
        return self.cart

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        return self.cart

    def get_totals(self):
        # Get product IDS
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart
        total = 0
        for key, value in cart.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        return total
