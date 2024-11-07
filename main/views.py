from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Product, Category, Comment , Color, Size
from .forms import CommentForm, ProductForm, CustomerForm
from django.contrib import messages
from django.contrib.auth.models import User

@login_required
def index(request):
    comments = Comment.objects.all()  
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user

            if not comment.product:
                comment.product = None  

            comment.save()

            messages.success(request, 'Your comment has been successfully added!')
            return redirect('main:index')   

    context = {
        'comments': comments,
        'form': form,
    }
    return render(request, 'index.html', context)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user == request.user:
        comment.delete()
        messages.success(request, 'Your comment has been successfully deleted.')
    else:
        messages.error(request, 'You can only delete your own comments.')

    return redirect('main:index')




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
    
    color = Color.objects.all()
    size = Size.objects.all()

    products = Product.objects.all()

    if selected_subtype:
        products = products.filter(category__subtype=selected_subtype)

    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query) |
            Q(category__subtype__icontains=query) 
        )
        color = color.filter(name__icontains=query)
        size = size.filter(size__icontains=query)


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
    comments = product.comments.all()
    form = CommentForm()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]

    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product  
            comment.save()
            messages.success(request, 'Your comment has been added.')
            
            return redirect('main:product_detail', product_id=product_id)

    context = {
        'product': product,
        'comments': comments,
        'form': form,
        'related_products': related_products,
    }

    return render(request, 'shop-single.html', context)
