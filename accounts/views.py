from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate 
from django.contrib import messages 
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from orders.models import Order, OrderItem
from shop.models import Product, Category
from django.db.models import Sum, F

# Create your views here.





def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('shop:shop')
        else:
            messages.error(request, "Please correct the errors before logging in")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {'form': form})


def login_view(request):
    if request.method == "POST":
        login = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(request, email= login, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back {user.username}!")
            next_url = request.GET.get('next', 'shop:shop')
            return redirect(next_url)

        messages.error(request, f"Invalid email or password!")
    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out!")
    return redirect('shop:shop')




@login_required
def dashboard(request):
    user = request.user
    context = {'user':user}

    # buyer dashboard 
    if user.role == "buyer":
        orders = Order.objects.filter(user=user)
        context.update({
            'orders':orders,
            'pending_orders':orders.filter(status='pending')

        })

    # vendor dashboard 
    elif user.role == "vendor":
        products = Product.objects.filter(user=user)
        categories = Category.objects.filter(user=user)

        # orders containng vedors product “Find orders where at least one item has a product owned by this user”
        # orders = Order.objects.filter(items__product__user=user).distinct() # this is correct but is not efficient it causes slow in db query and not advance . Query for each item → slow
        # it


        orders = Order.objects.filter(items__product__user=user).select_related('user').prefetch_related('items__product').distinct()
        # select_related for fk and one to one, prefetch for manay to manay and reverse fk - Loads all items + products in bulk → fast
        
        context.update({
            'products': products,
            'categories':categories,
            'orders': orders
        })

    else:

        from django.contrib.auth import get_user_model 
        User = get_user_model()
        orders= Order.objects.all()
        pending_orders = orders.filter(status='pending')
        completed_orders = orders.filter(status='completed')
        cancelled_orders = orders.filter(status='cancelled')
        paid_orders = orders.filter(status='paid')


        
        context.update({
            'products': Product.objects.all(),
            'categories': Category.objects.all(),
            'orders': Order.objects.all(),
            'users': User.objects.all(),
            'pending_orders': pending_orders,
            'completed_orders': completed_orders,
            'cancelled_orders': cancelled_orders,
            'paid_orders':paid_orders

        })



    
    
    return render(request, 'accounts/dashboard/dashboard.html', context)






from django.db.models import Sum

@login_required
def profile(request):
    user = request.user

    # Fetch unique orders for this user
    users = Order.objects.filter(user=user).order_by('id')[:1]
    # orders = Order.objects.filter(user=user).order_by('id')
    # total = sum([t for t in orders.total])
    # total = Order.objects.values('user__email').annotate(total_sum=Sum('total'))
    # total_sum = Order.objects.aggregate(total_sum=Sum('total'))
    total = Order.objects.filter(user=request.user).aggregate(total_sum=Sum('total'))
    total = total['total_sum']


    # {'total_sum': 100}
    # print(total_sum)

    context = {
        'user': user,
        'users': users,
        'total':total
    }
    return render(request, 'accounts/dashboard/profile.html', context)



@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email:
            request.user.email = new_email
            request.user.save()
            messages.success(request, "Email updated successfully!")
            return redirect('account_logout')  # or some success page
    return render(request, 'account/email.html')