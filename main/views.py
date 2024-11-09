from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db.models import Q
from .forms import CommentForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect , render
from .models import  Product, Category, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, DetailView, DeleteView

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been successfully added!')
            return redirect('main:index')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
    

# Logout View
def admin_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('main:index')

#login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(reverse('main:index'))  
        else:
            return render(request, ' login.html', {
                'error': 'Invalid username or password.'
            })
    
    return render(request,  'login.html')

# Delete Comment View
class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('main:index')

    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your comment has been successfully deleted.')
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, 'You can only delete your own comments.')
        return redirect('main:index')

# About View
class AboutView(TemplateView):
    template_name = 'about.html'

# Contact View
class ContactView(TemplateView):
    template_name = 'contact.html'
class ShopView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        selected_gender = self.request.GET.get('gender')
        selected_subtype = self.request.GET.get('subtype')
        sort_option = self.request.GET.get('sort')
        query = self.request.GET.get('q', '')

        products = Product.objects.all()

        if selected_gender:
            products = products.filter(gender=selected_gender)

        if selected_subtype:
            category = Category.objects.filter(subtype=selected_subtype).first()
            if category:
                products = products.filter(category=category)

        if query:
            products = products.filter(name__icontains=query)

        if sort_option == 'featured':
            products = products.filter(featured_product=True)
        elif sort_option == 'name':
            products = products.order_by('name')
        elif sort_option == 'price':
            products = products.order_by('-price')

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_gender'] = self.request.GET.get('gender')
        context['selected_subtype'] = self.request.GET.get('subtype')
        context['sort_option'] = self.request.GET.get('sort')  
        context['query'] = self.request.GET.get('q', '')   
        return context
    
# Shop Single Product Detail View
class ShopSingleView(DetailView):
    model = Product
    template_name = 'shop-single.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context

# Category List and Filter View
class CategoryListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        selected_subtype = self.request.GET.get('subtype', '')
        query = self.request.GET.get('q', '')
        sort_option = self.request.GET.get('sort', '')

        if selected_subtype:
            queryset = queryset.filter(category__subtype=selected_subtype)
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(brand__icontains=query) |
                Q(category__name__icontains=query) |
                Q(category__subtype__icontains=query) 
            )

        if sort_option == 'name':
            queryset = queryset.order_by('name')
        elif sort_option == 'featured':
            queryset = queryset.order_by('-rating')
        elif sort_option == 'price':
            queryset = queryset.order_by('-price')
        
        return queryset.prefetch_related('available_colors', 'images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gender_categories'] = Category.objects.filter(type='Gender')
        context['sale_categories'] = Category.objects.filter(type='Sale')
        context['product_categories'] = Category.objects.filter(type='Product')
        context['selected_subtype'] = self.request.GET.get('subtype', '')
        context['query'] = self.request.GET.get('q', '')
        context['sort_option'] = self.request.GET.get('sort', '')
        return context

# Filter Products by Category
class FilterProductsView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category__id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        return context

# Filter Products by Gender
class FilterProductsByGenderView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        gender = self.kwargs['gender']
        return Product.objects.filter(gender=gender)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gender'] = self.kwargs['gender']
        return context

# Product Detail View with Comments
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop-single.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = self.object
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('main:product_detail', product_id=self.object.id)

        context = self.get_context_data(form=form)
        return self.render_to_response(context)
