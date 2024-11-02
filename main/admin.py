from django.contrib import admin
from .models import Customer, Product, Category, ProductImage, Comment, Color, Size



# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Comment)
admin.site.register(Size)
admin.site.register(Color)

