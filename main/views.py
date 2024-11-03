from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Product, Category, Comment
from .forms import CommentForm , ProductForm, CustomerForm
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
    selected_gender = request.GET.get('gender')
    if selected_gender:
        products = products.filter(gender=selected_gender)   

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop.html', context)


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
        form = ProductForm(request.POST)   
        if form.is_valid():
            form.save()
            return redirect('main:shop')
    else:
        form = ProductForm() 

    return render(request, 'products/add_product.html', {'form': form})

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)   
        if form.is_valid():
            form.save()
            return redirect('main:customer_list')
    else:
        form = CustomerForm()   

    return render(request, 'customers/add_customer.html', {'form': form})

def category_list(request):
    gender_categories = Category.objects.filter(type='Gender')
    sale_categories = Category.objects.filter(type='Sale')
    product_categories = Category.objects.filter(type='Product')
    selected_subtype = request.GET.get('subtype')
    products = Product.objects.all()

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
    
    return render(request, 'shop.html', context)

def filter_products_by_gender(request, gender):
    products = Product.objects.filter(gender=gender)
    context = {
        'products': products,
        'gender': gender,
    }
    return render(request, 'shop.html', context)
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = product.comments.all()   
    form = CommentForm()

    specifications_list = product.specifications.split(',') if product.specifications else []
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]  

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product 
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('main:product_detail', product_id=product_id)

    context = {
        'product': product,
        'comments': comments,
        'form': form,
        'specifications_list': specifications_list,
        'related_products': related_products,   
    }
    return render(request, 'shop-single.html', context)

