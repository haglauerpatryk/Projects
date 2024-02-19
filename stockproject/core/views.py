from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")

def tables(request):
    return render(request, "tables.html")

def charts(request):
    return render(request, "charts.html")

def favourite(request):
    return render(request, "favourite.html")

def contact(request):
    return render(request, "contact.html")