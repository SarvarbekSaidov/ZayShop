from django.urls import path
from .views import index  , about, contact , shop , shop_single, product_list, add_product, customer_list, add_customer





app_name = 'main'  


urlpatterns = [
    path('', index, name='index'),   
    path('about/', about, name='about'),  
    path('contact/', contact, name='contact'),  
    path('shop/', shop, name='shop'),  
    path('shop-single/', shop_single, name='shop_single'), 
    path('products/', product_list, name='product_list'),   
    path('products/add/', add_product, name='add_product'),
    path('customers/', customer_list, name='customer_list'),  
    path('customers/add/', add_customer, name='add_customer'),   
]
