from .models import Category

def shop_context(request):
        """Inject categories and cart count into every template."""

        # return {
        #         'all_categories': Category.objects.all(),
        #         'cart_count': request.cart_count if hasattr(request, 'cart_count') else 0,
        # }

        cart = request.session.get('cart', {})

        return {
        "all_categories": Category.objects.all(),
        "cart_count": sum(cart.values()),
    }


from .models import Category

def categories(request):
    return {
        'categories': Category.objects.all()
    }


# settings.py — add to TEMPLATES['OPTIONS']['context_processors']

"""




"""