from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    # def add(self, product, quantity=1, override_qty=False):
    #     pk = str(product.pk)
    #     if pk not in self.cart:
    #         self.cart[pk] = 0
    #     if override_qty:
    #         self.cart[pk] = quantity
    #     else:
    #         self.cart[pk] += quantity
    #     self.save()

    def add(self, product, quantity=1, override_qty=False):
        pk = str(product.pk)

        if pk in self.cart:
            raise ValueError('Product already added')

        self.cart[pk] = quantity
        self.save()


    def increment(self, product):
        """Add 1, but never exceed available stock."""
        pk = str(product.pk)
        current = self.cart.get(pk, 0)
        if current < product.stock:           # ✅ respect stock limit
            self.cart[pk] = current + 1
            self.save()

    def decrement(self, product):
        """Remove 1; remove item entirely if qty reaches 0."""
        pk = str(product.pk)
        if pk in self.cart:
            self.cart[pk] -= 1
            if self.cart[pk] <= 0:
                del self.cart[pk]             # ✅ clean up zero-qty items
            self.save()

    def remove(self, product):
        pk = str(product.pk)
        if pk in self.cart:
            del self.cart[pk]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session['cart']
        self.save()

    def get_items(self):
        product_ids = [int(pk) for pk in self.cart.keys()]
        products = Product.objects.filter(pk__in=product_ids)
        items = []
        for product in products:
            qty = self.cart[str(product.pk)]
            items.append({
                'product': product,
                'qty': qty,
                'subtotal': product.effective_price * qty,
            })
        return items

    def get_total(self):
        return sum(item['subtotal'] for item in self.get_items())

    def get_count(self):
        return sum(self.cart.values())

    def __len__(self):
        return self.get_count()