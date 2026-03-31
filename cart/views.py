from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from shop.models import Product
from .cart import Cart
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required 
def cart_detail(request):
    from django.shortcuts import render
    cart = Cart(request)
    return render(request, "cart/cart.html", {"cart": cart})


# def cart_add(request, pk):
#     product = get_object_or_404(Product, pk=pk, is_active=True)
#     cart = Cart(request)
#     quantity = int(request.POST.get('quantity', 1))
#     try:
#         cart.add(product, quantity=quantity)
#         messages.success(request, f'{product.name} added to cart.')
#     except ValueError:
#         messages.warning(request, f'{product.name} already in cart.')
#     return redirect('shop:product-detail', pk=pk)


import json
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    
    cart = Cart(request)
    # quantity = int(request.POST.get('quantity', 1))
    data = json.loads(request.body)
    quantity = data.get('quantity')
    print(data)

    try:
        cart.add(product, quantity=quantity)
        messages.success(request, f'{product.name} added to cart.')
        return JsonResponse({'success':True, 'cart_count':cart.get_count()})
    except ValueError:
        messages.warning(request, f'{product.name} already in cart.')
        return JsonResponse({'success':False})

    # return redirect('shop:product-detail', pk=pk)







# def cart_remove(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     cart = Cart(request)
#     cart.remove(product)
#     messages.info(request, f'{product.name} removed from cart.')
#     if len(cart) == 0:
#         return redirect('shop:shop')
#     else:
#         return redirect('cart:detail')





def cart_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart(request)
    cart.remove(product)
    
    messages.info(request, f'{product.name} removed from cart.')

    return JsonResponse({
        'success': True,
        'cart_empty': len(cart) == 0,
        'cart_count': cart.get_count()

    })

    










# ✅ New views wired to the + / - buttons
# def cart_increment(request, pk):
#     product = get_object_or_404(Product, pk=pk, is_active=True)
#     cart = Cart(request)
#     cart.increment(product)
#     return redirect(request.META.get('HTTP_REFERER', 'shop:shop'))


def cart_increment(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    cart = Cart(request)
    cart.increment(product)

    return JsonResponse({
        'success': True,
        'cart_count': cart.get_count()
    })





# def cart_decrement(request, pk):
#     product = get_object_or_404(Product, pk=pk, is_active=True)
#     cart = Cart(request)
#     cart.decrement(product)
#     return redirect(request.META.get('HTTP_REFERER', 'shop:shop'))



def cart_decrement(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    cart = Cart(request)
    cart.decrement(product)

    
    return JsonResponse({
        'success': True,
        'cart_count': cart.get_count()
    })