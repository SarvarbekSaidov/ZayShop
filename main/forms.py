from django import forms
from .models import Comment, Product, Customer

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['first_name', 'last_name', 'text', 'rating']   

    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], label="Rating (1-5)")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'rating', 'brand', 'description', 'available_colors', 'specifications', 'sizes', 'quantity', 'price', 'featured_product', 'category', 'gender']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
