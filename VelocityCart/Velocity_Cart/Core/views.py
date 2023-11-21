from django.shortcuts import render
from .models import Product, Categorey
# Create your views here.

def Home(request):
    products = Product.objects.all()
    template = 'Core/home.html'
    context = {
        'products' : products,
    }
    return render(request, template, context)
