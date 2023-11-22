from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Categorey, CartItem, PurchaseProduct
from .forms import BuyForm
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


def cart(request):
    cart_items = CartItem.objects.all()
    template = 'Core/cart.html'
    context = {
        'cart_items' : cart_items,
    }
    return render(request, template, context)


def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    items = CartItem.objects.get_or_create(product=product, buyer_id=request.user.id)
    if not items:
        items.save()
    return redirect('/cart/')

def remove_from_cart(request, pk):
    product = Product.objects.get(id=pk)
    items = CartItem.objects.get(product=product)
    items.delete()
    return redirect('/cart/')

def checkout(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        form = BuyForm(request.POST)
        if form.is_valid():
            request.session['product'] = product.id
            request.session['buyer_name'] = form.cleaned_data['buyer_name']
            request.session['buyer_phone'] = form.cleaned_data['buyer_phone']
            request.session['buyer_email'] = form.cleaned_data['buyer_email']
            request.session['buyer_address'] = form.cleaned_data['buyer_address']
            return redirect('/buy-now/')
    else:
        form = BuyForm()
    template = 'Core/checkout.html'
    context = {
        'form' : form,
    }
    return render(request, template, context)

def buy_now(request):
    if request.method == "POST":
        answer = request.POST.get('answer')
        if answer == 'yes':
            product_id = request.session.get('product')
            if product_id is not None:
                product = get_object_or_404(Product, id=product_id)
                purchase_data, created = PurchaseProduct.objects.get_or_create(
                    product = product,
                    buyer_name = request.session.get('buyer_name'),
                    buyer_phone = request.session.get('buyer_phone'),
                    buyer_email = request.session.get('buyer_email'),
                    buyer_address = request.session.get('buyer_address')
                )
                if created:
                    purchase_data.save()
                    item = CartItem.objects.get(product=product)
                    item.delete()
                return redirect('/')
    template = 'Core/buye_now.html'
    return render(request, template)
