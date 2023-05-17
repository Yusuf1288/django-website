from django.shortcuts import render, get_object_or_404
from appStore.models import products
from category.models import *


# Create your views here.

def store(request, category_slug=None):
    categories = None
    Products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        Products = products.objects.filter(category=categories, is_available=True)
        Products_count = Products.count()
    else:
        Products = products.objects.all().filter(is_available=True)
        Products_count = Products.count()
    
    context = {

        'products': Products,
        'products_count': Products_count,

    }
    
    return render(request, 'appStore/store.html', context)

def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(products, category__slug=category_slug, slug=product_slug)
    context = {
        'single_product': single_product
    }
    return render(request, 'appStore/product_detail.html', context)
        