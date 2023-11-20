from django.shortcuts import render

# Create your views here.
def login(request):
    template = 'Auth/login.html'
    context = {
        'text':'This is login page!',
    }
    return render(request, template, context)
