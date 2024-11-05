from django.contrib import admin
from .models import Customer, Product, Category, ProductImage, Comment, Color, Size



# Register your models here.

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ProductImage)



class ProductImageInline(admin.TabularInline):
    model = Product.images.through
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
