from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Size(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
    ]
    
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)

    def __str__(self):
        return self.size

class Customer(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone Number")
    address = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    TYPE_CHOICES = [
        ('Gender', 'Gender'),
        ('Sale', 'Sale'),
        ('Product', 'Product'),
    ]
    SUBTYPE_CHOICES = {
        # 'Gender': [('Men', 'Men'), ('Women', 'Women')],
        'Sale': [('Sport', 'Sport'), ('Luxury', 'Luxury')],
        'Product': [('Clothes', 'Clothes'), ('Gadgets', 'Gadgets')],
    }

    name = models.CharField(max_length=100, verbose_name="Category Name", null=True) 
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Category Type", null=True)
    subtype = models.CharField(max_length=20, verbose_name="Category Subtype", null=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('unisex', 'Unisex'),
    ])

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if self.type is not None:
            valid_subtypes = dict(self.SUBTYPE_CHOICES.get(self.type, []))
            if self.subtype not in valid_subtypes:
                raise ValueError(f"Invalid subtype '{self.subtype}' for category type '{self.type}'.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.type} - {self.subtype}"

class Product(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    name = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    available_colors = models.ManyToManyField(Color, blank=True, verbose_name="Available Colors")   
    specifications = models.CharField(max_length=5000, null=True, blank=True)
    sizes = models.ManyToManyField(Size, blank=True, verbose_name="Available Sizes")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    featured_product = models.BooleanField(default=False, verbose_name="Featured Product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('unisex', 'Unisex')], null=True, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_gender_category(self):
        return self.category.subtype if self.category and self.category.type == 'Gender' else "Unspecified"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, default='default.jpg')

    def __str__(self):
        return f"Image for {self.product.name} (ID: {self.pk})"

from django.db import models

class Comment(models.Model):
    first_name = models.CharField(max_length=100,null=True)   
    last_name = models.CharField(max_length=100,null=True)    
    text = models.TextField()
    rating = models.IntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.text[:20]}...' 

