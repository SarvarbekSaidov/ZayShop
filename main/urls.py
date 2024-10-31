from django.urls import path
from .views import (
    index,
    about,
    contact,
    shop,
    shop_single,
    product_list,
    add_product,
    customer_list,
    add_customer,
    category_list,
    filter_products,
    product_detail,
)

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('shop/', category_list, name='shop'),
    path('shop-single/<int:product_id>/', product_detail, name='shop_single'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('products/add/', add_product, name='add_product'),
    path('customers/', customer_list, name='customer_list'),
    path('customers/add/', add_customer, name='add_customer'),
    path('categories/', category_list, name='category_list'),
    path('filter/<int:category_id>/', filter_products, name='filter_products'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),   
]
