from django.db import models

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
        'Gender': [('Men', 'Men'), ('Women', 'Women')],
        'Sale': [('Sport', 'Sport'), ('Luxury', 'Luxury')],
        'Product': [('Clothes', 'Clothes'), ('Gadgets', 'Gadgets')],
    }

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Category Type", null=True)
    subtype = models.CharField(max_length=20, verbose_name="Category Subtype", null=True)
    name = models.CharField(max_length=100, null=True)  

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        valid_subtypes = dict(self.SUBTYPE_CHOICES.get(self.type, []))
        if self.subtype not in valid_subtypes:
            raise ValueError(f"Invalid subtype '{self.subtype}' for category type '{self.type}'.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type} - {self.subtype}: {self.name}"


class Product(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    name = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    available_colors = models.CharField(max_length=200, verbose_name="Available Colors")   
    specifications = models.TextField()
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, default='static/assets/img/default.jpg')
    featured_product = models.BooleanField(default=False, verbose_name="Featured Product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products",null=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_gender_category(self):
        gender_category = self.category_set.filter(type='Gender').first()   
        return gender_category.subtype if gender_category else "Unspecified"
