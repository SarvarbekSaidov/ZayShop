from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Product, Category, Comment
from .forms import CommentForm  
from django.contrib import messages   

def index(request):
    comments = Comment.objects.all()   
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()   
            messages.success(request, 'Your comment has been successfully added!')
            return redirect('main:index')   
    context = {
        'comments': comments,
        'form': form,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()   
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'main/shop.html', context)

def shop_single(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop-single.html', {'product': product})

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
        specifications = request.POST['specification']
        size = request.POST['size']
        quantity = request.POST['quantity']
        price = request.POST['price']
        rating = request.POST['rating']
        
        Product.objects.create(
            brand=brand,
            description=description,
            available_colors=available_color,
            specifications=specifications,
            size=size,
            quantity=quantity,
            price=price,
            rating=rating
        )
        return redirect('main:shop')

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
        return redirect('main:customer_list')

    return render(request, 'customers/add_customer.html')

from django.shortcuts import render
from .models import Category, Product

def category_list(request):
    gender_categories = Category.objects.filter(type='Gender')
    sale_categories = Category.objects.filter(type='Sale')
    product_categories = Category.objects.filter(type='Product')
    selected_subtype = request.GET.get('subtype')
    products = Product.objects.all()
    if selected_subtype:
        products = products.filter(category__subtype=selected_subtype)

    for product in products:
        product.available_colors_list = product.available_colors.all() 
        product.images_list = product.images.all()  
    context = {
        'gender_categories': gender_categories,
        'sale_categories': sale_categories,
        'product_categories': product_categories,
        'products': products,
        'selected_subtype': selected_subtype,
    }

    return render(request, 'shop.html', context)

def filter_products(request, category_id):
    products = Product.objects.filter(category__id=category_id)
    
    context = {
        'products': products,
        'category_id': category_id,
    }
    
    return render(request, 'filtered_products.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = product.comments.all()
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return redirect('main:product_detail', product_id=product_id)

    context = {
        'product': product,
        'comments': comments,
        'form': form,
    }
    return render(request, 'shop-single.html', context)

