from django.forms import ModelForm
from .models import *

class ProductForm(ModelForm):
    class Meta:
        model= Product
        fields= "__all__"   # to filterout certain details we can use ['product_name','price']


class CategoryForm(ModelForm):
    class Meta:
        model= Category
        fields= "__all__"