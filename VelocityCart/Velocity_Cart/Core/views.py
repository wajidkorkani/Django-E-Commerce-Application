from django.shortcuts import render

# Create your views here.

def Home(request):
    template = 'Core/home.html'
    context = {
        'text' : 'Hello django!',
    }
    return render(request, template, context)
