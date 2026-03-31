from django.urls import path
from .views import  ProductDetailView, ProductListView,ProductUpdateView, CategoryDeleteView, TagDeleteView, ProductCreateView
from .views import TagCreateView,TagListView, TagUpdateView, ProductDeleteView, CategoryCreateView, CategoryListView, CategoryUpdateView
app_name = "shop"

urlpatterns = [
    path('', ProductListView.as_view(), name='shop'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name="product-detail"),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name="delete"),
    path('tag/', TagCreateView.as_view(), name="tag"),
    path('tag-list/', TagListView.as_view(), name='taglist'),
    path('tag-update/<int:pk>', TagUpdateView.as_view(), name='tagupdate'),
    path('tag-delete/<int:pk>', TagDeleteView.as_view(), name="tagdelete"),
    path('category/', CategoryCreateView.as_view(), name="category"),
    path('category-list/', CategoryListView.as_view(), name="categorylist"),
    path('category-update/<int:pk>', CategoryUpdateView.as_view(), name="categoryupdate"),
    path('category-delete/<int:pk>', CategoryDeleteView.as_view(), name='categorydelete')
    

]


