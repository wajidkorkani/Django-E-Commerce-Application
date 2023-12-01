from django.shortcuts import render, redirect

from Auth.forms import RigstrationForm

import random

from django.contrib.auth import (
    get_user_model,
    login,
    logout,
    authenticate
    )

# Create your views here.



def generate_otp():
    return str(random.randint(1000, 9999))


# Getting data from registration form filled by new user
def Registration(request):

    if request.method == "POST":
        form = RigstrationForm(request.POST)


        if form.is_valid():
            request.session['signup_otp'] = generate_otp()
            request.session["signup_username"] = form.cleaned_data['username']
            request.session["signup_email"] = form.cleaned_data['email']
            request.session['signup_fname'] = form.cleaned_data['first_name']
            request.session['signup_lname'] = form.cleaned_data['last_name']
            request.session['signup_password'] = form.cleaned_data['password1']
            return redirect('/otp/')


    else:
        form = RigstrationForm()



    template = 'Auth/signup_form.html'
    context = {
        'form': form,
    }
    return render(request, template, context)





# Verifying the otp code
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        form_otp = request.session['signup_otp']
        if otp == form_otp:                        # If the otp code given by user is equal to the which was generated
            User = get_user_model()


            user = User.objects.create_user(       # Storing information of user in the User model
                username = request.session.get('signup_username'),
                email = request.session.get('signup_email'),
                first_name = request.session.get('signup_fname'),
                last_name = request.session.get('signup_lname'),
                password = request.session.get('signup_password')
            )

            user.save()                           # Saving the user
            return redirect('/login/')


        else:
            form_otp = request.session['signup_otp']
            template = 'Auth/verify_otp.html'
            context = {
                'error_message': f"Invalid OTP | {form_otp}",
            }
            return render(request, template, context)



    form_otp = request.session['signup_otp']
    template = 'Auth/verify_otp.html'
    context = {
        'otp': form_otp,
    }
    return render(request, template, context)


 # Lging user in
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            template = 'Auth/login.html'
            context = {
                'error_message': 'Invalid email or password!'
            }
            return render(request, template, context)

    template = 'Auth/login.html'
    return render(request, template)


# Loging user out
def logout_user(request):
    logout(request)
    return redirect('/login/')
