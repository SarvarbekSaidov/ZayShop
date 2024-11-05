from django.urls import path
from .views import (
    index,
    about,
    contact,
    category_list,
    product_detail,
    filter_products,
    filter_products_by_gender,
)

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('shop/', category_list, name='shop'),
    path('shop-single/<int:product_id>/', product_detail, name='shop_single'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('filter/<int:category_id>/', filter_products, name='filter_products'),
    path('shop/<str:gender>/', filter_products_by_gender, name='filter_products_by_gender'),
]
