from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import account
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

class VariationManager(models.Manager):
    def colors(self):
        return self.filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return self.filter(variation_category='size', is_active=True)
    

variation_category_choice = (
    ('color','color'),
    ('size','size'),
)
class Variation(models.Model):
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ReviewRating(models.Model):
    product = models.ForeignKey(products, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    rating = models.FloatField()  # You might want to use choices here to limit to 1-5
    review = models.TextField(max_length=500, blank=True)
    ip = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.subject