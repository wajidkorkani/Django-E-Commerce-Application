from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Categorey
# Create your views here.

def Home(request):
    products = Product.objects.all()
    template = 'Core/home.html'
    context = {
        'products' : products,
    }
    return render(request, template, context)

def Product_About_Page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    template = 'Core/Product_About_Page.html'
    context = {
        'product' : product,
    }
    return render(request, template, context)

def Searchbar(request):
    if request.method == "GET":
        search = request.GET.get('search')
        products = Product.objects.filter(title__contains=search)
        product_categoery = Product.objects.filter(categorey__name__icontains=search)
        template = 'Core/Searchbar.html'
        context = {
            'products' : products,
        }
        return render(request, template, context)
