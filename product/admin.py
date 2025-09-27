from django.contrib import admin
from .models import Category, Product, Order, Contact

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Contact)
