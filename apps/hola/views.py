from django.shortcuts import render

# Create your views here.
def hola_mundo(request):
    return render(request, 'hola/index.html');
