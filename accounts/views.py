from ordering.models import *
import requests
from .forms import UserProfileForm
from appStore.models import *
from carts.views import _cart_id
from carts.models import *
from django.shortcuts import render,redirect
from accounts.models import * 
from .forms import RegistrationForm
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from .forms import AccountForm, UserProfileForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = account.objects.create_user(first_name=first_name, last_name=last_name,phone_number=phone_number,email=email,password=password, username=username)
            user.phone_number = phone_number
            user.save()

            #user activation
            current_site = get_current_site(request)
            mail_subject ='Please activate your Account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message, to=[to_email])
            send_email.send()
           # messages.success(request, 'Registration Successfully ')
            return redirect('/accounts/login/?command=verification&email='+ email )
    else:
        form = RegistrationForm()
    
    context = {
        'form': form
    }

    return render(request, "accounts/register.html", context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            try:
                guest_cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=guest_cart).exists()

                if is_cart_item_exists:
                    guest_cart_items = CartItem.objects.filter(cart=guest_cart)

                    # Get or create a new Cart instance for the user
                    user_cart, created = Cart.objects.get_or_create(user=user)

                    # Get all cart items of the user
                    user_cart_items = CartItem.objects.filter(user=user)

                    for guest_item in guest_cart_items:
                        # Check if the logged-in user already has this item in their cart
                        # Considering the product and variations

                        same_item_in_user_cart = None
                        for user_item in user_cart_items:
                            if (user_item.product == guest_item.product and 
                                set(user_item.variations.all()) == set(guest_item.variations.all())):
                                same_item_in_user_cart = user_item
                                break

                        if same_item_in_user_cart:
                            # User already has this item (with the same variations) in their cart, 
                            # so update the quantity
                            same_item_in_user_cart.quantity += guest_item.quantity
                            same_item_in_user_cart.save()
                        else:
                            # User doesn't have this item (or these variations) in their cart, 
                            # so let's add it
                            guest_item.user = user
                            guest_item.cart = user_cart
                            guest_item.save()

            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage= params['next']
                    return redirect (nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')



@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged Out')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError, account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations!!! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def dashboard(request):
    orders = Order.objects.order_by('created_at').filter(user_id = request.user.id)
    orders_count = orders.count()

    context = {
        'orders_count': orders_count,
    }
    return render(request, 'accounts/dashboard.html', context)


def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=False).order_by('-created_at')
    print(orders)
    return render(request, 'accounts/my_orders.html', {'orders': orders})

def profile_update(request):
    return render(request, 'accounts/profile_update.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if account.objects.filter(email=email).exists():
            user = account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject ='Reset Your Password'
            message = render_to_string('accounts/reset_password.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset link has been sent to your email ')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError, account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your Password ')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('login')
    
def resetPassword(request):

    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword') 
    else:
        return render(request, 'accounts/resetPassword.html')

def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,'accounts/profile.html',{'user_profile':user_profile})




@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = AccountForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.first_name = user_form.cleaned_data['first_name'] or user.first_name
            user.last_name = user_form.cleaned_data['last_name'] or user.last_name
            user.phone_number = user_form.cleaned_data['phone_number'] or user.phone_number
            user.email = user_form.cleaned_data['email'] or user.email
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = AccountForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user = account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')

