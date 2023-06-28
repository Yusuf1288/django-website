from .models import *
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render,redirect
from .forms import OrderForm
from .models import Order
from carts.models import CartItem
from accounts.models import account
from django.template.loader import get_template
import pdfkit
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from django.template.loader import render_to_string

def download_invoice(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    template = get_template('ordering/order_complete.html')
    html_string = template.render({'order': order})
    
    # add path to wkhtmltopdf
    path_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    # pass the configuration to the method
    pdf = pdfkit.from_string(html_string, False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=order_complete.pdf'
    
    return response

# Create your views here.
def payments(request):

    return render(request, 'ordering/payments.html')

def order_complete(request):
    current_user = request.user
    order = Order.objects.filter(user=current_user).last()  # Fetches the most recent order for the current user
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    

    if cart_count <= 0:
        return redirect('home:index')
    
    total = 0
    quantity = 0
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = 0.165 * total
    grand_total = tax + total

    if order:
        context = {'order': order,
                'tax': tax,
                'total':total,
                'grand_total':grand_total,
                'quantity':quantity,
                'cart_items':cart_items,}
    else:
        messages.error(request, 'No completed orders found.')
        context = {}

    
    return render(request, 'ordering/order_complete.html',context)


def orderingFunction(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('home:index')
    
    total = 0
    quantity = 0
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = 0.165 * total
    grand_total = tax + total

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.district = form.cleaned_data['district']
            data.region = form.cleaned_data['region']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            d = timezone.now()
            current_date = d.strftime("%Y%m%d") # YYYYMMDD

            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number= order_number)

            context = {
                'order': order,
                'tax': tax,
                'total':total,
                'grand_total':grand_total,
                'quantity':quantity,
                'cart_items':cart_items,

            }

            return render(request,'ordering/payments.html',context)
        else:
            messages.error(request, 'There was an error processing your form.')
            return render(request, 'appStore/ordering.html', {'form': form, 'cart_items': cart_items})

    else:  
        form = OrderForm()

            
        
    return render(request, 'ordering.html',{'form':form,  'cart_items': cart_items,'grand_total':grand_total} )







