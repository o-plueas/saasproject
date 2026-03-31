from django  import forms 
from .models import Product, Category, Tag 


class ProductForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # slug = forms.SlugField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    # # description = forms.TextInput(widget=forms.Textarea(attrs={'class':'form-control'}))
    # # price = forms.DecimalField(widget=forms.FloatField(attrs={'class':'form-control'}))
    # sale_price = forms.DecimalField(widget=forms.FloatField(attrs={'class':'form-control'}))
    # is_active = forms.BooleanField(widget=forms.BooleanField(attrs={'class':'form-control'}))
    # stock = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    # image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Product 
        fields = '__all__' 







class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    slug= forms.SlugField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image=forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'image']


class TagForm(forms.ModelForm):
    class Meta:

        model = Tag
        fields = ['name']
        name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
