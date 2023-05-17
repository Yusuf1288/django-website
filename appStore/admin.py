from django.contrib import admin
from .models import products

# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display = ('name','price','category','stock','modified_date','is_available')
    prepopulated_fields = {'slug':('name',)}

admin.site.register(products, productAdmin)