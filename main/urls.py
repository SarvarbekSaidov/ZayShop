from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect
from .views import (
    IndexView,
    AboutView,
    ContactView,
    ShopView,
    ShopSingleView,
    CategoryListView,
    ProductDetailView,
    FilterProductsView,
    FilterProductsByGenderView,
    DeleteCommentView,
)
from . import views

app_name = 'main'

def admin_logout(request):
    logout(request)
    return redirect('/admin/login/')

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  
    path('about/', AboutView.as_view(), name='about'),  
    path('contact/', ContactView.as_view(), name='contact'),  
    path('shop/', ShopView.as_view(), name='shop'),  
    path('shop-single/<int:product_id>/', ShopSingleView.as_view(), name='shop_single'),  
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),  
    path('filter/<int:category_id>/', FilterProductsView.as_view(), name='filter_products'),  
    path('shop/<str:gender>/', FilterProductsByGenderView.as_view(), name='filter_products_by_gender'),  
    path('delete_comment/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),  
    path('admin-logout/', admin_logout, name='admin_logout'),
]
