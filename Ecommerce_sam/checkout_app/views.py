import hmac

from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum
from cart_app.models import Cart_products, Cart_model
import razorpay
from Ecommerce_sam import settings

def checkout(request):
    if 'available_cart_pk' in request.session:
        cart_objs = Cart_products.objects.filter(cart_id=Cart_model.objects.get(id=request.session['available_cart_pk'],is_payment_done=False).id)
        cart_item_exist = True if cart_objs.count()>0 else False
        total_product_cost = cart_objs.aggregate(Sum('product_cost'))
    elif request.user.is_authenticated :
        cart_objs = Cart_products.objects.filter(cart_id=Cart_model.objects.get(user_id=request.user.id,is_payment_done=False).id)
        cart_item_exist = True if cart_objs.count() > 0 else False
        total_product_cost=cart_objs.aggregate(Sum('product_cost'))

    context={
        'cart_objs':cart_objs,
        'cart_item_exist':cart_item_exist,
        'total_product_cost':total_product_cost['product_cost__sum'],
    }
    return render(request,'main/Checkout_main.html',context)

def payment(request):
    if request.method == 'POST' and 'csrfmiddlewaretoken' in request.POST and 'total_product_cost' in request.POST:
        client = razorpay.Client(auth=(settings.KEY_ID_RAZORPAY, settings.KEY_SECRET_RAZORPAY))
        client.set_app_details({"title": "Moms_Veggies", "version": "0.1"})


        DATA = {"amount": int(float(str(request.POST.get('total_product_cost'))))*100,
                "currency": "INR",
                "receipt": 'order_rcptid_11',
                "payment_capture": "1",
                "notes": {
                    "business_id": 'no',

                }
                }

        order_id_razorpay=client.order.create(data=DATA)
        print(order_id_razorpay['id'])
        print(order_id_razorpay)


        if 'available_cart_pk' in request.session:
            cart_objs = Cart_products.objects.filter(cart_id=Cart_model.objects.get(id=request.session['available_cart_pk'],is_payment_done=False).id)
            cart_item_exist = True if cart_objs.count()>0 else False
            total_product_cost = cart_objs.aggregate(Sum('product_cost'))
        elif request.user.is_authenticated :
            cart_objs = Cart_products.objects.filter(cart_id=Cart_model.objects.get(user_id=request.user.id,is_payment_done=False).id)
            cart_item_exist = True if cart_objs.count() > 0 else False
            total_product_cost=cart_objs.aggregate(Sum('product_cost'))

        context={
            'name':str(request.POST.get('billing_first_name'))+str(request.POST.get('billing_last_name')),
            'email': request.POST.get('billing_email'),
            'phone': request.POST.get('billing_phone'),
            'total_product_cost': request.POST.get('total_product_cost'),
            'cart_objs': cart_objs,
            'cart_item_exist': cart_item_exist,
            'order_id_razorpay': order_id_razorpay['id'],
        }
        return render(request,'payment/payment.html',context)
    else:
        return HttpResponse("Something Went Wrong, Try Again!!!")

def payment_confirmation(request):
    if request.method == 'POST' and 'razorpay_order_id' in request.POST:
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        print("razorpay_order_id + + razorpay_payment_id + + settings.KEY_SECRET_RAZORPAY:")
        print(razorpay_order_id + "|" + razorpay_payment_id + "|" + settings.KEY_SECRET_RAZORPAY)
        print(":razorpay_signature:")
        print(razorpay_signature)
        import hashlib
        key = bytes(settings.KEY_SECRET_RAZORPAY, 'utf-8')
        msg = "{}|{}".format(razorpay_order_id, razorpay_payment_id)
        body = bytes(msg, 'utf-8')

        dig = hmac.new(key=key,
                       msg=body,
                       digestmod=hashlib.sha256)

        generated_signature = dig.hexdigest()
        print(":generated_signature:")
        print(generated_signature)
        if (generated_signature == razorpay_signature):
            print("payment is Successful")
            payment = True
        else:
            print("payment is Unsuccessful")
            payment = False


        import razorpay
        client = razorpay.Client(auth=(settings.KEY_ID_RAZORPAY, settings.KEY_SECRET_RAZORPAY))
        data=client.payment.fetch(razorpay_payment_id)
        if payment and data['order_id']==razorpay_order_id and data['id']==razorpay_payment_id and data['status']== 'captured' and data['error_code'] == None:
            final_payment_status = True
        else:
            final_payment_status = False

        context = {
            'final_payment_status':final_payment_status,
        }
        return render(request, 'payment/payment_validation.html', context)
    else:
        return HttpResponse("Something Went Wrong, Try Again!!!")


