from django.db.models import Q
from django.shortcuts import render, redirect

from cart_app.models import Cart_model, Cart_products

# from user_app.models import Track_User
from .models import Product_model
from django.core.paginator import Paginator

def all_products(request):
    products_list = Product_model.objects.all()
    paginator = Paginator(products_list, 9)
    page = request.GET.get('page')
    products_list = paginator.get_page(page)
    context={}
    # if request.method == 'GET' and 'orderby' in request.GET:
    #     orderby = request.GET.get('orderby')
    #     if orderby == 'price':
    #         products_list = Product_model.objects.all().order_by('selling_cost')
    #     elif orderby == 'rating':
    #         products_list = Product_model.objects.all().order_by('ratings')
    #     elif orderby == 'date':
    #         products_list = Product_model.objects.all().order_by('entry_timedate')
    #     elif orderby == 'price-desc':
    #         products_list = Product_model.objects.all().order_by('-selling_cost')
    #     elif orderby == 'popularity':
    #         products_list = Product_model.objects.all().order_by('popularity')
    #     paginator = Paginator(products_list, 9)
    #     page = request.GET.get('page')
    #     products_list = paginator.get_page(page)
    #     context22 = {'all_products': products_list, }
    #     context.update(context22)
    #     # return redirect('/')



    context2={
        'all_products':products_list,
    }
    context.update(context2)
    return render(request,'main/all_products.html',context)

def product_detail(request,slug):
    product = Product_model.objects.get(slug=slug)
    context = {}
    recmonded_products = Product_model.objects.filter(~Q(slug=slug)).order_by('popularity')[0: 5]
    if request.method == 'POST' and 'add-to-cart' in request.POST:
        quantity = request.POST.get('quantity')
        product_id = request.POST.get('product_id')
        if request.user.is_authenticated:
            available_cart = Cart_model.objects.filter(user_id=request.user.pk,is_payment_done=False)
            if available_cart.count()>0:
                for item in available_cart:
                    main_c_pk = item.pk
                item = Cart_products()
                item.product = Product_model.objects.get(id=product_id)
                item.product_quantity = quantity
                item.cart_id = Cart_model.objects.get(id=main_c_pk)
                item.product_cost = Product_model.objects.get(id=product_id).selling_cost * quantity
                item.save()
            else:
                main_cart = Cart_model()
                main_cart.total_cost = 0.0
                main_cart.total_quantity = 0.0
                main_cart.user_id = request.user.pk
                main_cart.save()

                item = Cart_products()
                item.product = Product_model.objects.get(id=product_id)
                item.product_quantity = quantity
                item.cart_id = Cart_model.objects.get(id=main_cart.pk)
                item.product_cost = Product_model.objects.get(id=product_id).selling_cost * quantity
                item.save()

        else:
            if 'available_cart_pk' in request.session:

                item = Cart_products()
                item.product = Product_model.objects.get(id=product_id)
                item.product_quantity = quantity
                item.cart_id = Cart_model.objects.get(id=request.session['available_cart_pk'])
                item.product_cost = Product_model.objects.get(id=product_id).selling_cost * float(quantity)
                item.save()
            elif 'available_cart_pk' not in request.session:
                if not request.session.session_key:
                    request.session.create()
                session_id = request.session.session_key
                main_cart = Cart_model()
                main_cart.total_cost = 0.0
                main_cart.total_quantity = 0.0
                main_cart.session_id = session_id
                main_cart.save()

                request.session['available_cart_pk']= main_cart.pk

                item = Cart_products()
                item.product = Product_model.objects.get(id=product_id)
                item.product_quantity = quantity
                item.cart_id = Cart_model.objects.get(id=main_cart.pk)
                item.product_cost = float(Product_model.objects.get(id=product_id).selling_cost) * float(quantity)
                item.save()

        request.session['in_cart']=True
        # request.session['in_cart'].set_expiry(60)
        return redirect('/product_detail/'+str(product.slug))

    context2={
        'product':product,
        'recmonded_products':recmonded_products,
    }
    context.update(context2)
    return render(request, 'main/product_detail.html', context)
