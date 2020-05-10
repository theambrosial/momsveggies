from django.shortcuts import render

def home(request):
    return render(request,'main/home.html')

def all_products(request):
    return render(request,'main/all_products.html')


def cart(request):
    return render(request,'main/cart.html')

def checkout(request):
    return render(request,'main/Checkout_main.html')

def product_detail(request):
    return render(request,'main/product_detail.html')
