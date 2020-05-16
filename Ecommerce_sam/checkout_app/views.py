import hmac

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum
from cart_app.models import Cart_products, Cart_model
import razorpay
from Ecommerce_sam import settings
from .models import Orders_rzp, Order_placed, payment_rzp


def checkout(request):
    if 'available_cart_pk' in request.session:
        cart_objs = Cart_products.objects.filter(cart_id=Cart_model.objects.get(id=request.session['available_cart_pk'],is_payment_done=False).id)
        cart_item_exist = True if cart_objs.count()>0 else False
        total_product_cost = cart_objs.aggregate(Sum('product_cost'))

    elif request.user.is_authenticated :
        cart_model = Cart_model.objects.filter(user_id=request.user.id, is_payment_done=False)
        if cart_model.count() > 0:
            for item in cart_model:
                cart_pk = item.pk
            cart_objs = Cart_products.objects.filter(cart_id=cart_pk)
            cart_item_exist = True if cart_objs.count() > 0 else False
            total_product_cost = cart_objs.aggregate(Sum('product_cost'))
        else:
            cart_objs = None
            cart_item_exist = False
            total_product_cost = {'product_cost__sum': 0}
    else:
        cart_objs = None
        cart_item_exist = False
        total_product_cost = {'product_cost__sum': 0}

    context={
        'cart_objs':cart_objs,
        'cart_item_exist':cart_item_exist,
        'total_product_cost':total_product_cost['product_cost__sum'],
    }
    return render(request,'main/Checkout_main.html',context)

def payment(request):
    if request.method == 'POST' and 'csrfmiddlewaretoken' in request.POST and 'total_product_cost' in request.POST:
        # Creating User In The Database
        from user_app.models import SiteUser
        if request.user.is_authenticated:
            user = request.user
        else:
            if SiteUser.objects.filter(email=request.POST.get('billing_email')).count()>0:
                request.POST = request.POST
                if 'available_cart_pk' in request.session:
                    cart_objs = Cart_model.objects.filter(id=request.session['available_cart_pk'],
                                                          is_payment_done=False)
                    cart_objs.update(user_id=request.user.id)
                    cart_objs = Cart_products.objects.filter(
                        cart_id=Cart_model.objects.get(id=request.session['available_cart_pk'], is_payment_done=False).id)
                    cart_item_exist = True if cart_objs.count() > 0 else False
                elif request.user.is_authenticated:
                    cart_objs = Cart_products.objects.filter(
                        cart_id=Cart_model.objects.get(user_id=request.user.id, is_payment_done=False).id)
                    cart_item_exist = True if cart_objs.count() > 0 else False
                context = {

                    'total_product_cost': request.POST.get('total_product_cost'),
                    'cart_objs': cart_objs,
                    'cart_item_exist': cart_item_exist,
                    'user_already_exist_email': True,
                    'user_already_email': request.POST.get('billing_email')

                }
                return render(request, 'main/Checkout_main.html', context)
            elif SiteUser.objects.filter(mobile=request.POST.get('billing_phone')).count()>0:
                if 'available_cart_pk' in request.session:
                    cart_objs = Cart_model.objects.filter(id=request.session['available_cart_pk'],
                                                          is_payment_done=False)
                    cart_objs.update(user_id=request.user.id)
                    cart_objs = Cart_products.objects.filter(
                        cart_id=Cart_model.objects.get(id=request.session['available_cart_pk'], is_payment_done=False).id)
                    cart_item_exist = True if cart_objs.count() > 0 else False
                elif request.user.is_authenticated:
                    cart_objs = Cart_products.objects.filter(
                        cart_id=Cart_model.objects.get(user_id=request.user.id, is_payment_done=False).id)
                    cart_item_exist = True if cart_objs.count() > 0 else False
                context = {
                    'total_product_cost': request.POST.get('total_product_cost'),
                    'cart_objs': cart_objs,
                    'cart_item_exist': cart_item_exist,
                    'user_already_exist_phone': True,
                    'user_already_phone': request.POST.get('billing_phone')

                }
                return render(request, 'main/Checkout_main.html', context)
            generated_password = str(request.POST.get('billing_first_name'))[:3]+str(request.POST.get('billing_phone'))[5:]
            user = SiteUser()
            user.email = request.POST.get('billing_email')
            user.set_password(generated_password)
            user.mobile = request.POST.get('billing_phone')
            user.first_name = request.POST.get('billing_first_name')
            user.last_name = request.POST.get('billing_last_name')
            user.password_text = generated_password
            user.save()
            # Logging User In System
            user = authenticate(request, mobile=request.POST.get('billing_phone'), password=generated_password)
            if user is not None:
                login(request, user)

            # Emailing Credentials To The User
            from common_utilities.email_utility import send_html_mail
            html_content='''
            <p>UserName : '''+request.POST.get('billing_phone')+'''</p>
            <p>Password : '''+generated_password+'''</p>
            <p> Thank You</p>
            '''
            send_html_mail('Account Created - Moms Veggies',html_content,settings.EMAIL_HOST_USER,[request.POST.get('billing_email'),])
        #Creating RayzorPay Order
        client = razorpay.Client(auth=(settings.KEY_ID_RAZORPAY, settings.KEY_SECRET_RAZORPAY))
        client.set_app_details({"title": "Moms_Veggies", "version": "0.1"})
        DATA = {"amount": int(float(str(request.POST.get('total_product_cost'))))*100,
                "currency": "INR",
                "receipt": 'order_rcptid_11',
                "payment_capture": "1",}
        order_id_razorpay=client.order.create(data=DATA)

        orders_rzp = Orders_rzp()
        orders_rzp.user_id = user
        orders_rzp.amount = order_id_razorpay['amount']
        orders_rzp.razorpay_order_id = order_id_razorpay['id']
        orders_rzp.razorpay_order_id = ''
        orders_rzp.razorpay_payment_id = ''
        orders_rzp.razorpay_signature = ''
        orders_rzp.generated_signature = ''
        orders_rzp.signature_matching_status = False
        orders_rzp.is_payment_successful = False
        orders_rzp.save()

        orders = Order_placed()
        orders.user_id = user
        orders.fname = request.POST.get('billing_first_name')
        orders.lname = request.POST.get('billing_last_name')
        orders.phone = request.POST.get('billing_phone')
        orders.email = request.POST.get('billing_email')
        orders.city = request.POST.get('billing_city')
        orders.state = request.POST.get('billing_state')
        orders.zip_code = request.POST.get('billing_postcode')
        orders.address1 = request.POST.get('billing_address_1')
        orders.address2 = request.POST.get('billing_address_2')
        orders.country = request.POST.get('billing_country')
        orders.order_rzp_id = orders_rzp
        orders.delivery_status = 'Preparing Order'
        orders.delivery_done = False
        orders.save()

        if request.user.is_authenticated:
            cart_latest = Cart_model.objects.filter(user_id=request.user.id, is_payment_done=False).order_by('-id')[0]
            cart_objs = Cart_products.objects.filter(
                cart_id=cart_latest.id)
            cart_item_exist = True if cart_objs.count() > 0 else False
            total_product_cost = cart_objs.aggregate(Sum('product_cost'))

        elif 'available_cart_pk' in request.session:
            cart_objs = Cart_model.objects.filter(id=request.session['available_cart_pk'], is_payment_done=False).order_by('-id')[0]
            cart_objs.update(user_id=request.user.id)
            cart_objs = Cart_products.objects.filter(cart_id=cart_objs.id)

            cart_item_exist = True if cart_objs.count()>0 else False
            total_product_cost = cart_objs.aggregate(Sum('product_cost'))

        # elif request.user.is_authenticated :
        #     cart_objs = Cart_products.objects.filter(cart_id=Cart_model.objects.get(user_id=request.user.id,is_payment_done=False).id)
        #     cart_item_exist = True if cart_objs.count() > 0 else False
        #     total_product_cost=cart_objs.aggregate(Sum('product_cost'))

        # cart_model_obj = Cart_model.objects.get(user_id=request.user.id,is_payment_done=False)

        context={
            'name':str(request.POST.get('billing_first_name'))+str(request.POST.get('billing_last_name')),
            'email': request.POST.get('billing_email'),
            'phone': request.POST.get('billing_phone'),
            'total_product_cost': request.POST.get('total_product_cost'),
            'cart_objs': cart_objs,
            'cart_item_exist': cart_item_exist,
            'order_id_razorpay': order_id_razorpay['id'],
            'orders_rzp': orders_rzp,
            'orders': orders,
        }
        return render(request,'payment/payment.html',context)
    else:
        return HttpResponse("Something Went Wrong, Try Again!!!")

def payment_confirmation(request,orders_rzp, orders):
    if request.method == 'POST' and 'razorpay_order_id' in request.POST:
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        # Veryfing Payment Status by matching razorpay signature
        import hashlib
        key = bytes(settings.KEY_SECRET_RAZORPAY, 'utf-8')
        msg = "{}|{}".format(razorpay_order_id, razorpay_payment_id)
        body = bytes(msg, 'utf-8')
        dig = hmac.new(key=key,msg=body,digestmod=hashlib.sha256)
        generated_signature = dig.hexdigest()

        if (generated_signature == razorpay_signature):
            print("payment is Successful")
            payment = True
            Orders_rzp.objects.filter(id = int(orders_rzp)).update(razorpay_order_id=razorpay_order_id,razorpay_payment_id=razorpay_payment_id,razorpay_signature=razorpay_signature,generated_signature=generated_signature,signature_matching_status=True,is_payment_successful=True)
            Order_placed.objects.filter(id = int(orders)).update(payment_status=True,order_rzp_id=Orders_rzp.objects.get(id = int(orders_rzp)))
        else:
            print("payment is Unsuccessful")
            payment = False
            Orders_rzp.objects.filter(id = int(orders_rzp)).update(razorpay_order_id=razorpay_order_id,razorpay_payment_id=razorpay_payment_id,razorpay_signature=razorpay_signature,generated_signature=generated_signature,signature_matching_status=False,is_payment_successful=False)
            Order_placed.objects.filter(id = int(orders)).update(payment_status=False,order_rzp_id=Orders_rzp.objects.get(id = int(orders_rzp)))


        client = razorpay.Client(auth=(settings.KEY_ID_RAZORPAY, settings.KEY_SECRET_RAZORPAY))
        data=client.payment.fetch(razorpay_payment_id)
        if payment and data['order_id']==razorpay_order_id and data['id']==razorpay_payment_id and data['status']== 'captured' and data['error_code'] == None:
            final_payment_status = True
            cart_model_obj = Cart_model.objects.filter(user_id=request.user.id, is_payment_done=False)
            for item in cart_model_obj:
                cart_model_id = item.id
            cart_objs_c = Cart_products.objects.filter(cart_id=cart_model_id).aggregate(Sum('product_cost'))
            cart_objs_q = Cart_products.objects.filter(cart_id=cart_model_id).aggregate(Sum('product_quantity'))
            cart_model_obj.update(is_payment_done=True,total_cost=cart_objs_c['product_cost__sum'],total_quantity=cart_objs_q['product_quantity__sum'])

            rzp_payment = payment_rzp()
            rzp_payment.razorpay_payment_id = razorpay_payment_id
            rzp_payment.final_payment_confirmation = True
            rzp_payment.user_id = request.user
            rzp_payment.razorpay_status = data['status']
            rzp_payment.order_rzp_id = Orders_rzp.objects.get(id = int(orders_rzp))
            rzp_payment.order_placed_id = Order_placed.objects.get(id = int(orders))
            rzp_payment.cart_model_id = Cart_model.objects.get(id=cart_model_id)
            rzp_payment.save()

            from common_utilities.email_utility import send_html_mail
            html_content = '''
                        <p>Payment Successful</p>
                        <p> Thank You</p>
                        '''
            send_html_mail('Payment Successful - Moms Veggies', html_content, settings.EMAIL_HOST_USER,
                           [request.user.email, ])

        else:
            final_payment_status = False
            cart_model_obj = Cart_model.objects.filter(user_id=request.user.id, is_payment_done=False)
            for item in cart_model_obj:
                cart_model_id = item.id
            rzp_payment = payment_rzp()
            rzp_payment.razorpay_payment_id = 'Failure' if razorpay_payment_id == None or razorpay_payment_id == '' else razorpay_payment_id
            rzp_payment.final_payment_confirmation = False
            rzp_payment.user_id = request.user
            rzp_payment.razorpay_status = data['status']
            rzp_payment.order_rzp_id = Orders_rzp.objects.get(id=int(orders_rzp))
            rzp_payment.order_placed_id = Order_placed.objects.get(id=int(orders))
            rzp_payment.cart_model_id = Cart_model.objects.get(id=cart_model_id)
            rzp_payment.save()
            from common_utilities.email_utility import send_html_mail
            html_content = '''
                                    <p>Payment Unsuccessful</p>
                                    <p> Thank You</p>
                                    '''
            send_html_mail('Payment Unsuccessful - Moms Veggies', html_content, settings.EMAIL_HOST_USER,
                           [request.user.email, ])


        context = {
            'final_payment_status':final_payment_status,
        }
        return render(request, 'payment/payment_validation.html', context)
    else:
        return HttpResponse("Something Went Wrong, Try Again!!!")


