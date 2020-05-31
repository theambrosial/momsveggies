from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from cart_app.models import Cart_products

from Ecommerce_sam import settings
from common_utilities.email_utility import send_html_mail

from .models import SiteUser
from django.utils.http import is_safe_url

def home(request):
    return render(request,'main/home.html')

def product_detail(request):
    return render(request,'main/product_detail.html')


def about_us(request):
    return render(request,'main/about.html')

def logout_user(request):

    logout(request)
    return redirect('/')

def lost_password(request):
    if request.method == 'POST':
        user_login = request.POST.get('user_login')
        if SiteUser.objects.filter(email=user_login).count()>0:
            generated_password = SiteUser.objects.get(email=user_login)
            generated_password2 = generated_password.mobile[:5]+generated_password.email[:2]+generated_password.first_name[:1]
            user = SiteUser.objects.get(email=user_login)
            user.password_text = generated_password2
            user.set_password(generated_password2)
            user.save(update_fields=['password_text','password'])

            html_content = '''
                        <p>Login Using Below Password:</p>
                        <p>Login Url: http://tsit.pythonanywhere.com/account/ </p>
                        <p>Password : ''' + generated_password2 + '''</p>
                        <p> Thank You</p>
                        '''
            send_html_mail('Password Reset Request - Moms Veggies', html_content, settings.EMAIL_HOST_USER,
                           [user_login, ])
            context = {
                'exist_email': True,
                'user_already_email': user_login

            }
            return render(request, 'auth/lost_password.html', context)
        else:

            context = {
                'user_does_exist_email': True,
                'user_already_email': user_login

            }
            return render(request, 'auth/lost_password.html',context)

    return render(request,'auth/lost_password.html')

def account(request):
    if request.user.is_authenticated:
        cart_objs = Cart_products.objects.filter(cart_id__user_id=request.user,cart_id__is_payment_done=True)
        context={
            'cart_objs':cart_objs,
        }
        return render(request,'main/account.html',context)
    else:
        if request.method == 'POST':
            print(request.POST)
            if 'username' in request.POST :
                username = request.POST.get('username')
                password = request.POST.get('password')

                # Logging User In System
                user = authenticate(request, mobile=username, password=password)
                if user is not None:
                    login(request, user)
                    next = request.GET.get('next', '/')
                    if not is_safe_url(next, allowed_hosts=None):
                        next = '/'
                    return redirect(next)
                    # return redirect('/account/')
                else:

                    context = {
                        'does_not_exist_user': True,
                        'cart_objs': None,
                    }
                    return render(request, 'main/account.html', context)

            if 'fname' in request.POST:
                fname = request.POST.get('fname')
                lname = request.POST.get('lname')
                email = request.POST.get('email')

                SiteUser.objects.filter(id=request.user.pk).update(first_name=fname,last_name=lname,email=email)
                print("hhihihihihih")

        context = {
            'cart_objs': None,
        }
        return render(request, 'main/account.html', context)


def delete_cart_item(request):
    if request.method == 'GET' and 'id' in request.GET and request.GET.get("q")!= None:
        cart_id = request.GET.get("q", None)
        cart_pro_id = request.GET.get("id", None)
        Cart_products.objects.filter(id=cart_pro_id).delete()
        print("execut")
        return redirect('/cart')

def delete_item(request):
    if request.method == 'GET' and 'id' in request.GET and request.GET.get("q")!= None:
        cart_id = request.GET.get("q", None)
        cart_pro_id = request.GET.get("id", None)
        Cart_products.objects.filter(id=cart_pro_id).delete()
        print("execut")
        return redirect('/')

