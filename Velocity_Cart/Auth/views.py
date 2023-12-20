from django.shortcuts import render, redirect

import random

from django.contrib.auth import (
    get_user_model,
    login,
    logout,
    authenticate
    )

from django.core.mail import send_mail

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
    )


# Create your views here.

# Generate OTP code
def generate_otp():
    return str(random.randint(1000, 9999))



def Registration(request):

    if request.method == "POST":

        # Getting data from form
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        otp = generate_otp()

        # If the username is already in use
        if get_user_model().objects.filter(username=username).exists():
            form = RigstrationForm()
            template = 'Auth/signup_form.html'
            context = {
                'error_message' : 'Sorry this user name is already in use.',
                "error_message2" : "Please try an other username."
            }
            return render(request, template, context)


        # If the email is already in use
        elif get_user_model().objects.filter(email=email).exists():   # If the email is already in use than user will not be able to create an account.

            template = 'Auth/signup_form.html'
            context = {
            'error_message': 'Sorry this email is already in use.',
            'error_message2': 'Please try and other email.',
            }
            return render(request, template, context)


        # If first name field is empty
        elif len(first_name) <= 1 :
            template = 'Auth/signup_form.html'
            context = {
                'error_message' : "Sorry first name can't be empty.",
                "error_message2" : "Please fill all the fields."
            }
            return render(request, template, context)


        # If last name field is empty
        elif len(last_name) < 1 :
            template = 'Auth/signup_form.html'
            context = {
                'error_message' : "Sorry last name can't be empty.",
                "error_message2" : "Please fill all the fields."
            }
            return render(request, template, context)



        # If both passwords are not same
        elif password1 != password2:
            template = 'Auth/signup_form.html'
            context = {
                'error_message' : 'Sorry passwords are not same.',
                "error_message2" : "Please make sure that both passwords are same."
            }
            return render(request, template, context)


        # If password is less than eight characters
        elif len(password1) < 8:
            template = 'Auth/signup_form.html'
            context = {
                'error_message' : 'Weak password',
                "error_message2" : "Your password must be equal to the 8 characters."
            }
            return render(request, template, context)


        # If everthing is fine than the proccess will be continue and OTP code email will be sent to the user on given email by user after entering the wright OTP code user account will be created.
        else:
            send_mail(
                'Velocity Cart otp',
                f'This is your otp to create your account on Velocity Cart: {otp}',
                'Velocity Cart',
                [email],
                fail_silently=False,
            )
            request.session['signup_otp'] = otp
            request.session["signup_username"] = username.lower()
            request.session["signup_email"] = email
            request.session['signup_fname'] = first_name
            request.session['signup_lname'] = last_name
            request.session['signup_password'] = password1
            return redirect('/otp/')


    template = 'Auth/signup_form.html'
    return render(request, template)






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
            return redirect('/accounts/login/')


        else:
            form_otp = request.session['signup_otp']
            template = 'Auth/verify_otp.html'
            context = {
                'error_message': f"Invalid OTP",
            }
            return render(request, template, context)



    form_otp = request.session['signup_otp']
    template = 'Auth/verify_otp.html'
    context = {
        'otp': 'Please enter OTP code we sent to your email account.',
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
    return redirect('/accounts/login/')




# Password reset section
class CustomPasswordResetView(PasswordResetView):
    template_name = 'Auth/password_reset_form.html'
    email_template_name = 'Auth/password_reset_email.html'
    success_url = '/password_reset/done/'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'Auth/password_reset_done.html'



class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'Auth/password_reset_confirm.html'
    success_url = '/reset/done/'



class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'Auth/password_reset_complete.html'
