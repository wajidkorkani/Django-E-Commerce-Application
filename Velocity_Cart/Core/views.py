from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
    )

from .models import (
    Product,
    Categorey,
    CartItem,
    PurchaseProduct,
    HomePageImage,
    ProductComments,
    CommentReply,
    Ratings
    )

from django.utils import timezone

from django.contrib.auth.models import User

from .forms import BuyForm

from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
# Create your views here.


# Home page
def Home(request):
    images = HomePageImage.objects.all()   #   Getting the banner

    # If user is uploading new banner without deleting the old banner than old banner will be deleted automatically
    if images.count() > 1:
        excess_images = images[:1]         # Getting the new banner and deleting the old banner
        for img in excess_images:
            img.delete()

    image = images.first()

    products = Product.objects.all()       # Getting the all products

    # Render the template with the data
    template = 'Core/home.html'
    context = {
        'products': products,
        'poster': image,
    }
    return render(request, template, context)




# Searchbar

def Searchbar(request):
    if request.method == "POST":
        search = request.POST['search']
        products = Product.objects.filter(title__contains=search) # if text searched by user is = or contain title of any existing proudct than that product will be show on the browser page
        product_categoery = Product.objects.filter(categorey__name__icontains=search) # if text searched by user is = or contain title of any existing proudct than that product will be show on the browser page
        template = 'Core/Searchbar.html'
        context = {
            'products' : products,
            'product_categoery' : product_categoery,
        }
        return render(request, template, context)



# Product section

def Product_About_Page(request, product_id):

    ratings_box = []            # Here in this  list we will store all the ratings of product
    product = get_object_or_404(Product, id=product_id)
    ratings = Ratings.objects.filter(product=product) # We are geting ratings of the product

    for r in ratings:         # Storing all the ratings in list
        ratings_box.append(r.rate)

    if ratings_box:            # Geting average ratings of the product
        product_rating = round(sum(ratings_box) / len(ratings_box), 1)
    else:
        product_rating = 0.0    # If product is new or product has no ratings yet than rating of product will be 0.0


    category = product.categorey.name
    comments = ProductComments.objects.filter(product=product)
    related_products = Product.objects.filter(categorey__name=category)

    template = 'Core/Product_About_Page.html'
    context = {
        'product': product,
        'related_products': related_products,
        'comments': comments,
        'ratings': product_rating,
    }

    return render(request, template, context)



# Retreving comment replys of the product
def Comments_Replys_Page(request, pk):
    comment = get_object_or_404(ProductComments, id=pk)
    replys = CommentReply.objects.filter(comment=comment)
    template = 'Core/comments_replys.html'
    context = {
        'comment' : comment,
        'replys' : replys,
    }
    return render(request, template, context)



# Adding comments on the proudct
@login_required
def Product_Comments(request, pk):
    url = request.META.get('HTTP_REFERER')   #  Getting the current page url
    if request.method == "POST":
        form = request.POST['comment']
        data, created = ProductComments.objects.get_or_create(
            product = get_object_or_404(Product, id=pk),
            user = request.user,
            comment = form,
            time_stamp = timezone.now(),
        )
        if created:
            data.save()
        return redirect(url)
    else:
        return redirect(url)



# Adding comment replys
@login_required
def Comments_Replys(request, pk):
    url = request.META.get('HTTP_REFERER')    #  Getting the current page url
    if request.method == "POST":
        form = request.POST['reply']
        data, created = CommentReply.objects.get_or_create(
            comment = get_object_or_404(ProductComments, id=pk),
            user = request.user,
            reply = form,
            time_stamp = timezone.now(),
        )
        if created:
            data.save()
        return redirect(url)
    else:
        return redirect(url)





# Product rating section

# Here I am adding the ratings in the product
def Product_Ratings(request, pk):

    if request.method == "POST":

        # Getting all the ratings chossen by user
        one = request.POST.get('one', 0)
        two = request.POST.get('two', 0)
        three = request.POST.get('three', 0)
        four = request.POST.get('four', 0)
        five = request.POST.get('five', 0)
        six = request.POST.get('six', 0)
        seven = request.POST.get('seven', 0)
        eight = request.POST.get('eight', 0)
        nine = request.POST.get('nine', 0)
        ten = request.POST.get('ten', 0)

        # Adding or storing all the ratings in one variable
        number = float(one)+float(two)+float(three)+float(four)+float(five)+float(six)+float(seven)+float(eight)+float(nine)+float(ten)


        # Counting the ratings and applying the condition
        if number == 5:
            stars = 5
        elif number == 4:
            stars = 4
        elif number == 3:
            stars = 3
        elif number == 2:
            stars = 2
        elif number == 1:
            stars = 1
        elif number == 0.5:
            stars = 0.5
        elif number == 1.5:
            stars = 1.5
        elif number == 2.5:
            stars = 2.5
        elif number == 3.5:
            stars = 3.5
        elif number == 4.5:
            stars = 4.5
        else:
            stars = 0


        # Getting the product
        product = get_object_or_404(Product, id=pk)
        user = request.user # Getting the current user or user who requested or adding the ratings

        # Storing all the ratings in the Ratings model
        rate, created = Ratings.objects.get_or_create(
            product = product,
            user = user,
            rate = stars,
        )

        if created:             # Saving the ratings
            rate.save()

        return redirect('/')    # Redirecting the user to the homepage




# This is the page where user will rate the product
@login_required
def user_giving_ratings_to_the_product_from_page(request):
    user = request.user
    product_id = request.session.get('product')


    if product_id is not None and isinstance(product_id, int):
        product = get_object_or_404(Product, id=product_id)
        purchased_product = PurchaseProduct.objects.filter(buyer=request.user, product=product).first()

        request.session.pop('product', None)

        template = 'Core/Give_Ratigs_to_the_Product.html'
        context = {
            'product': product,
            'id': product.id,
            'purchased': purchased_product
        }
        return render(request, template, context)

    else:
        # Handle the case when product_id is not valid (optional)
        return HttpResponse("Invalid product ID or missing product ID in session.")




# Cart section
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(buyer=request.user.id)
    template = 'Core/cart.html'
    context = {
        'cart_items' : cart_items,
    }
    return render(request, template, context)



# Adding the proudct to the cart of requested user or current usr
def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    items = CartItem.objects.get_or_create(product=product, buyer_id=request.user.id)
    if not items:
        items.quantity += 1
        items.save()
    return redirect('/cart/')



# Removing product from cart of request user or current usre
def remove_from_cart(request, pk):
    product = Product.objects.get(id=pk)
    items = CartItem.objects.filter(product=product, buyer=request.user)
    for item in items:
        item.delete()
    return redirect('/cart/')



def remove_all_items_from_cart(request):
    items = CartItem.objects.filter(buyer=request.user)
    for item in items:
        item.delete()
    return redirect('/cart/')



# product purchase section

# User will checkout for only single prodcut user want to buy and minimun quantity of the product must be greater than 0
@login_required
def checkout(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == "POST":
        form = BuyForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > 0:                              #   Checking if the quantity of the product is greater than 0 otherwise user will get an error message
                request.session['product'] = product.id
                request.session['product_quantity'] = quantity
                request.session['product_size'] = form.cleaned_data['size']
                request.session['product_color'] = form.cleaned_data['color']
                request.session['buyer_phone'] = form.cleaned_data['buyer_phone']
                request.session['buyer_email'] = form.cleaned_data['buyer_email']
                request.session['buyer_address'] = form.cleaned_data['buyer_address']
                return redirect('buy_now')

            else:
                form = BuyForm()

            template = 'Core/checkout.html'
            context = {
                'form': form,
                'error_message' : 'Sorry, Product quantity must be more than 0.'
            }

            return render(request, template, context)


    else:
        form = BuyForm()

    template = 'Core/checkout.html'
    context = {'form': form}
    return render(request, template, context)



# Buying the product
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
                        product=product,
                        product_id_number=product.id,
                        buyer=buyer,
                        buyer_name=f"{buyer.first_name} {buyer.last_name}",
                        registration_email=buyer.email,
                        quantity=request.session.get('product_quantity'),
                        color=request.session.get('product_color'),
                        size=request.session.get('product_size'),
                        buyer_phone=request.session.get('buyer_phone'),
                        buyer_email=request.session.get('buyer_email'),
                        buyer_address=request.session.get('buyer_address'),
                        time_stamp=timezone.now()
                    )

                    if created:
                        purchase_data.save()

                        try:
                            items = CartItem.objects.filter(product=product)
                            for item in items:
                                item.delete()

                        except CartItem.DoesNotExist:
                            pass
                    quantity=request.session.get('product_quantity')
                    color=request.session.get('product_color')
                    size=request.session.get('product_size')
                    buyer_phone=request.session.get('buyer_phone')
                    buyer_email=request.session.get('buyer_email')
                    buyer_address=request.session.get('buyer_address'),


                    send_mail(
                        'Product Details',
                        f"Thanks for shopping {request.user.first_name} {request.user.last_name} \n Here are product details \n Name : {product.title} \n Quantity : {quantity} \n Color : {color} \n Size : {size} \n Total price : ${quantity * product.price}  \n Your phone number : {buyer_phone} \n Your email address : {buyer_email} \n Your address : {buyer_address} \n Payment : Payment is on delivery. \n Delivery : The product will be deliverd within 10 days to the given address. \n Thanks for shopping. \n Thanks for testing this Velocity Cart and of course this was just a test email and this product will not be delivered to you. ",
                        'Velocity Cart',
                        [buyer_email, request.user.email],
                        fail_silently=False,
                    )


                    send_mail(
                        'Product Details',
                        f"{request.user.first_name} {request.user.last_name} has just placed his/her first order \n Here are product details \n Name : {product.title} \n Quantity : {quantity} \n Color : {color} \n Size : {size} \n Total price : ${quantity * product.price}  \n Phone number : {buyer_phone} \n Registared email address : {request.user.email} \n Given Email address : {buyer_email} \n Address : {buyer_address} \n Delivery : The product must be deliverd within 10 days to the given address.",
                        'Velocity Cart',
                        {'Your email here'},
                        fail_silently=False,
                    )


                    return redirect('/give-ratings/')

            elif answer == 'no':
                return redirect('cart')

        template = 'Core/buye_now.html'
        return render(request, template)
