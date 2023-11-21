from django.shortcuts import render, redirect
from Auth.forms import RigstrationForm
import random
from django.contrib.auth import get_user_model, login as login_user, logout, authenticate
# Create your views here.

def generate_otp():
    return str(random.randint(1000, 9999))

def Registration(request):
    if request.method == "POST":
        form = RigstrationForm(request.POST)
        if form.is_valid():
            request.session['signup_otp'] = generate_otp()
            request.session["signup_username"] = form.cleaned_data['username']
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


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        form_otp = request.session['signup_otp']
        if otp == form_otp:
            User = get_user_model()
            user = User.objects.create_user(
                username = request.session.get('signup_username'),
                first_name = request.session.get('signup_fname'),
                last_name = request.session.get('signup_lname'),
                password = request.session.get('signup_password')
            )
            user.save()
            return redirect('/login/')
    else:
        form_otp = request.session['signup_otp']
        template = 'Auth/verify_otp.html'
        context = {
            'otp': f"Invalid OTP \{form_otp}",
        }
        return render(request, template, context)
    form_otp = request.session['signup_otp']
    template = 'Auth/verify_otp.html'
    context = {
        'otp': form_otp,
    }
    return render(request, template, context)



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_user(request, user)
            return redirect('/')
        else:
            template = 'Auth/login.html'
            context = {
                'error_message':'Invalid email or password!'
            }
            return render(request, template, context)
    template = 'Auth/login.html'
    return render(request, template)

def login_user(request):
    logout(request)
    return redirect('/login/')
