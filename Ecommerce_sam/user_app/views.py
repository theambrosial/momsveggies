from django.shortcuts import render

def home(request):
    return render(request,'main/home.html')


def product_detail(request):
    return render(request,'main/product_detail.html')
