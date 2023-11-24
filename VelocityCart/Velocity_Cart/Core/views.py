from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Categorey, CartItem, PurchaseProduct, HomePageImage
from .forms import BuyForm
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.

def Home(request):
    images = HomePageImage.objects.all()

    if images.count() > 1:
        excess_images = images[:1]
        for img in excess_images:
            img.delete()

    image = images.first()

    products = Product.objects.all()

    # Render the template with the data
    template = 'Core/home.html'
    context = {
        'products': products,
        'poster': image,
    }
    return render(request, template, context)


def Product_About_Page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categorey = product.categorey.name
    related_products = Product.objects.filter(categorey__name=categorey)
    template = 'Core/Product_About_Page.html'
    context = {
        'product' : product,
        'related_products' : related_products,
    }
    return render(request, template, context)


def Searchbar(request):
    if request.method == "POST":
        search = request.POST['search']
        products = Product.objects.filter(title__contains=search)
        product_categoery = Product.objects.filter(categorey__name__icontains=search)
        template = 'Core/Searchbar.html'
        context = {
            'products' : products,
            'product_categoery' : product_categoery,
        }
        return render(request, template, context)


def cart(request):
    cart_items = CartItem.objects.filter(buyer=request.user.id)
    template = 'Core/cart.html'
    context = {
        'cart_items' : cart_items,
    }
    return render(request, template, context)


def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    items = CartItem.objects.get_or_create(product=product, buyer_id=request.user.id)
    if not items:
        items.quantity += 1
        items.save()
    return redirect('/cart/')

def increase_quantity(request, pk):
    product = Product.objects.get(id=pk)
    items = CartItem.objects.get_or_create(product=product, buyer_id=request.user.id)
    if not items:
        item = items
        item.quantity += 1
        item.save()
    return redirect('cart')


def remove_from_cart(request, pk):
    product = Product.objects.get(id=pk)
    items = CartItem.objects.filter(product=product, buyer=request.user)
    for item in items:
        item.delete()
    return redirect('/cart/')

def checkout(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        form = BuyForm(request.POST)
        if form.is_valid():
            request.session['product'] = product.id
            request.session['product_quantity'] = form.cleaned_data['quantity']
            request.session['product_color'] = form.cleaned_data['color']
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
            cart_id = request.session.get('cart')
            if product_id is not None:
                product = get_object_or_404(Product, id=product_id)
                buyer = get_object_or_404(User, id=request.user.id)
                purchase_data, created = PurchaseProduct.objects.get_or_create(
                    product = product,
                    product_id_number = product.id,
                    buyer = buyer,
                    buyer_name = f"{buyer.first_name} {buyer.last_name}",
                    registration_email = buyer.email,
                    quantity = request.session.get('product_quantity'),
                    color = request.session.get('product_color'),
                    buyer_phone = request.session.get('buyer_phone'),
                    buyer_email = request.session.get('buyer_email'),
                    buyer_address = request.session.get('buyer_address'),
                    time_stamp = timezone.now()
                )
                if created:
                    purchase_data.save()
                    try:
                        item = CartItem.objects.get(product=product)
                        item.delete()
                    except:
                        pass
                return redirect('/')
        elif answer == 'no':
            return redirect('/cart/')
    template = 'Core/buye_now.html'
    return render(request, template)
