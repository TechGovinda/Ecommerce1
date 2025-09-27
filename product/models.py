from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    uploaded_at= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    description = models.TextField()
    quantity = models.IntegerField()
    image = models.FileField(upload_to='static/uploads',null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    
class Order(models.Model):
    PAYMENT_METHOD= (
        ('Cash on Delevery', 'Cash on Delivery'),
        ('Esewa', 'Esewa'),
        ('Khalti', 'Khalti')
    )
    product= models.ForeignKey(Product, on_delete = models.CASCADE)
    total_price = models.IntegerField()
    quantity = models.IntegerField()
    payment_method= models.CharField(choices=PAYMENT_METHOD, max_length=200)
    payment_status= models.CharField(default='Pending', max_length=200)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email= models.EmailField()
    
    
    
class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # auto timestamp

    def __str__(self):
        return f"{self.name} - {self.email}"