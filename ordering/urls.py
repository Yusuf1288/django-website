from django.urls import path
from .  import views





app_name = 'ordering'

urlpatterns = [
    path('payments/', views.payments, name='payments'),
    path('place_order/', views.orderingFunction, name='orderingFunction'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('download_invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),



]

