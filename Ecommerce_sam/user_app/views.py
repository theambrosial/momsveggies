from django.shortcuts import render, redirect
from cart_app.models import Cart_products


def home(request):
    return render(request,'main/home.html')

def product_detail(request):
    return render(request,'main/product_detail.html')

def account(request):
    return render(request,'main/account.html')

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

