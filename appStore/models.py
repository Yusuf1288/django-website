from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.


class products(models.Model):
    name = models.CharField(max_length=100, unique=True)                
    description = models.TextField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug,self.slug]) 
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name
    


    