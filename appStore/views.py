from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from appStore.models import products
from category.models import *
from carts.models import *
from carts.views import _cart_id
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
# Create your views here.

def store(request, category_slug=None):
    categories = None
    Products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        Products = products.objects.filter(category=categories, is_available=True)
        paginator = Paginator(Products, 6) 
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        Products_count = Products.count()
    else:
        Products = products.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(Products, 6) 
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        Products_count = Products.count()
        
    
    context = {

        'products': paged_products,
        'products_count': Products_count,

    }
    
    return render(request, 'appStore/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = get_object_or_404(products, category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
            'single_product': single_product,
            'in_cart':in_cart ,
         }
    return render(request, 'appStore/product_detail.html', context)

def search(request):
    products_list = products.objects.all()
    products_count = products_list.count()  # default value

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products_list = products.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q (name__icontains=keyword))
            products_count = products_list.count()  # update if keyword is present

    context = {
        'products': products_list,
        'products_count': products_count,
    }
    return render(request, 'appStore/store.html', context)



        