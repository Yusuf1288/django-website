from .models import ReviewRating
from django.contrib import admin
from .models import products,Variation

# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display = ('name','price','category','stock','modified_date','is_available')
    prepopulated_fields = {'slug':('name',)}
admin.site.register(products, productAdmin)
class VariationAdmin(admin.ModelAdmin):
    list_display= ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')
admin.site.register(Variation,VariationAdmin)

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'rating', 'ip', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'review', 'user__username')

admin.site.register(ReviewRating, ReviewRatingAdmin)



