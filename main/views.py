from django.shortcuts import render,redirect
from .models import Customer, Product
from django.http import HttpResponse


# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')  

def shop(request):
    return render(request, 'shop.html')

def shop_single(request):
    return render(request, 'shop-single.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

def add_product(request):
    if request.method == 'POST':
        brand = request.POST['brand']
        description = request.POST['description']
        available_color = request.POST['available_color']
        specification = request.POST['specification']
        size = request.POST['size']
        quantity = request.POST['quantity']
        price = request.POST['price']
        rating = request.POST['rating']
        
        Product.objects.create(
            brand=brand,
            description=description,
            available_color=available_color,
            specification=specification,
            size=size,
            quantity=quantity,
            price=price,
            rating=rating
        )
        return redirect('shop.html')   

    return render(request, 'products/add_product.html')

def add_customer(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')

        Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address
        )
        return redirect('customer_list')  

    return render(request, 'customers/add_customer.html')
