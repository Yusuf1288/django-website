from django.shortcuts import render
from appStore.models import products

# Create your views here.

def home(request):
    Products = products.objects.all().filter(is_available=True)
    context = {

        'products': Products,

    }
        
    
    return render(request, 'index.html', context)