from django.contrib import admin
from .models import Payment, Order, OrderProduct

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'amount_paid', 'payment_method', 'status', 'created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'first_name', 'last_name', 'phone', 'email', 'country', 'district', 'region',
                    'address', 'order_total', 'tax', 'status', 'is_ordered', 'created_at', 'updated_at']

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'payment', 'user', 'color', 'Variation', 'quantity', 'product_price', 'ordered',
                    'created_at', 'updated_at']
