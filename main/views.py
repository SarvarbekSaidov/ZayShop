from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Product, Category, Comment
from .forms import CommentForm, ProductForm, CustomerForm
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
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]   

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop-single.html', context)

def category_list(request):
    gender_categories = Category.objects.filter(type='Gender')
    sale_categories = Category.objects.filter(type='Sale')
    product_categories = Category.objects.filter(type='Product')
    selected_subtype = request.GET.get('subtype', '')
    query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', '')

    products = Product.objects.all()

    if selected_subtype:
        products = products.filter(category__subtype=selected_subtype)

    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )

    if sort_option == 'name':
        products = products.order_by('name')
    elif sort_option == 'featured':
        products = products.order_by('-rating')
    elif sort_option == 'price':
        products = products.order_by('-price')
        
    products = products.prefetch_related('available_colors', 'images')

    context = {
        'gender_categories': gender_categories,
        'sale_categories': sale_categories,
        'product_categories': product_categories,
        'products': products,
        'selected_subtype': selected_subtype,
        'query': query,
        'sort_option': sort_option,
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
    
    # Fetch comments related to the product
    comments = product.comments.all()
    
    # Create a new comment form
    form = CommentForm()

    # Split specifications into a list
    specifications_list = product.specifications.split(',') if product.specifications else []

    # Get related products from the same category, excluding the current product
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]

    # Handle POST request for adding a comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create a new comment without saving it to the database yet
            comment = form.save(commit=False)
            comment.product = product  # Associate the comment with the current product
            comment.save()  # Save the comment to the database
            messages.success(request, 'Your comment has been added.')  
            return redirect('main:product_detail', product_id=product_id)  

    context = {
        'product': product,
        'comments': comments,
        'form': form,
        'specifications_list': specifications_list,
        'related_products': related_products,
    }
    
    # Render the template with the context
    return render(request, 'shop-single.html', context)