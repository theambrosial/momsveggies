from django.db.models import Sum
from django.shortcuts import render
from .models import Cart_model, Cart_products
import datetime


def cart(request):
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

    return render(request,'main/cart.html',context)


def notification_context(request):
    if request.user.is_authenticated :
        cart = Cart_model.objects.filter(user_id=request.user.id,is_payment_done=False)
        if cart.exists() and cart!= None and cart.count() > 0:
            for item in cart:
                cart_id = item.id
            cart_objs = Cart_products.objects.filter(cart_id=cart_id)
            cart_item_count_notif = cart_objs.count()
            cart_items_notif = cart_objs
            total_product_cost = cart_objs.aggregate(Sum('product_cost'))
            return {
                'is_cart_items_notif': True,
                'cart_items_notif': cart_items_notif,
                'cart_item_count_notif': cart_item_count_notif,
                'total_product_cost': total_product_cost['product_cost__sum'],
            }
        else:
            return {
                'is_cart_items_notif': False,
                'cart_item_count_notif': 0,
                'total_product_cost': 0,
            }
    elif 'available_cart_pk' in request.session:
        cart = Cart_model.objects.filter(id=request.session['available_cart_pk'],is_payment_done=False)
        if cart.exists() and cart != None and cart.count() > 0:
            for item in cart:
                cart_id = item.id
            cart_objs = Cart_products.objects.filter(cart_id=cart_id)
            cart_item_count_notif = cart_objs.count()
            cart_items_notif = cart_objs
            total_product_cost = cart_objs.aggregate(Sum('product_cost'))

            return {
                'is_cart_items_notif': True,
                'cart_items_notif': cart_items_notif,
                'cart_item_count_notif': cart_item_count_notif,
                'total_product_cost': total_product_cost['product_cost__sum'],
            }
        else:
            return {
                'is_cart_items_notif': False,
                'cart_item_count_notif': 0,
                'total_product_cost': 0,
            }

    else:
        return {
            'is_cart_items_notif': False,
            'cart_item_count_notif': 0,
            'total_product_cost': 0,
        }

