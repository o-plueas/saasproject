from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.db.models import Q 
from .models import Product, Category, Tag
from .forms import TagForm, CategoryForm, ProductForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required 
from django.core.exceptions import PermissionDenied 

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 12 

    def get_queryset(self):
        qs =  Product.objects.filter(is_active=True).select_related('categories')
        print(qs)

        # Search 
        q = self.request.GET.get('q', '')

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        
        # category filter 

        cat = self.request.GET.get('category', '')
        if cat:
            qs = qs.filter(categories__slug=cat)

            # price sort 
        sort = self.request.GET.get('sort', '-created_at')

        if sort in ['price', '-price', '-created_at', 'name']:
            qs = qs.order_by(sort)

        return qs 
    

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        ctx['query'] = self.request.GET.get('q', '')
        ctx['cart_count'] = self.get_cart_count()

        return ctx
    def get_cart_count(self):
        cart = self.request.session.get('cart', {})
        return sum(cart.values())


# @method_decorator(login_required, name="dispatch")
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('categories').prefetch_related('tags')
        
        cat = self.request.GET.get('category', '')
        if cat:
            qs = qs.filter(categories__slug=cat)
            
        return qs
    


@method_decorator(login_required, name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/products/product-form.html'
    success_url =  reverse_lazy('shop:shop')


    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully')
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Create Form'
        context['label'] = 'Create Product'

        return context 
    


@method_decorator(login_required, name="dispatch")
class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product 
    form_class = ProductForm 
    template_name = 'shop/products/product-form.html'
    success_url = reverse_lazy('shop:shop')

    def form_valid(self, form):
        messages.success(self.request, 'Updated successfully')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Product Form'
        context['label'] = 'Update'
        return context
    
    def test_func(self):
        product = self.get_object()
        return product.user == self.request.user

# @method_decorator(login_required, name="dispatch")
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'shop/products/product-confirm-delete.html'
    success_url = reverse_lazy('shop:shop')

    def test_func(self):
        product = self.get_object()
        return product.user == self.request.user



@method_decorator(login_required, name="dispatch")
class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = "shop/tags/tag-form.html"
    success_url = reverse_lazy('shop:taglist')

    def form_valid(self, form):
        messages.success(self.request, 'Tags created successfully')
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['label'] = 'Create Tag'
        context['title'] = 'Create Tag Form'
        return context        
    


class TagListView(ListView):
    model = Tag 
    template_name = 'shop/tags/tag-list.html'
    context_object_name = 'tags'
    paginate_by = 12 

    def get_queryset(self):
        qs = Tag.objects.all()
        return qs
    
@method_decorator(login_required, name="dispatch")
class TagUpdateView(UserPassesTestMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'shop/tags/tag-form.html'
    success_url = reverse_lazy('shop:taglist')

    def form_valid(self, form):
        messages.success(self.request, 'Tag updated successfully')

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['label'] = 'Update Tag'
        context['title'] = 'Update Tag Form'
        return context
    
    def test_func(self):
        tag = self.get_object()
        return tag.user == self.request.user

# @method_decorator(login_required, name="dispatch")
class TagDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tag 
    template_name = 'shop/tags/tag_confirm_delete.html'
    success_url = reverse_lazy('shop:taglist')
    
    def test_func(self):
        tag = self.get_object()
        return tag.user == self.request.user


@method_decorator(login_required, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "shop/category/category-form.html"
    success_url = reverse_lazy('shop:categorylist')

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully')
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['label'] = 'Create Category'
        context['title'] = 'Create Category Form'
        return context        
    

class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category/category-list.html'
    context_object_name = 'categories'
    paginate_by = 12 

    def get_queryset(self):
        qs = Category.objects.all()
        return qs
    

@method_decorator(login_required, name="dispatch")
class CategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm 
    template_name = 'shop/category/category-form.html'
    success_url = reverse_lazy('shop:categorylist')

    def get_context_data(self, **kwargs):
    
        context = super().get_context_data(**kwargs)
        context['title'] ='Update Category Form'
        context['label'] = 'Update Category'
        return context 

    def test_func(self):
        category = self.get_object()
        return category.user == self.request.user



@method_decorator(login_required, name="dispatch")
class CategoryDeleteView(UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'shop/category/category_confirm_delete.html'
    success_url = reverse_lazy('shop:categorylist')


    def test_func(self):
        category = self.get_object()
        return category.user == self.request.user





def custom_permission_denied_view(request, exception=None):
    context ={
        'user': request.user,

    }

    return render(request, '403.html', context, status=403)