class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
 
    def __call__(self, request):
        # Code BEFORE the view runs
        cart = request.session.get('cart', {})
        request.cart_count = sum(cart.values())
 
        response = self.get_response(request)
 
        # Code AFTER the view runs
        return response
 
