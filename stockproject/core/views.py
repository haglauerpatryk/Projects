from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")

def tables(request):
    return render(request, "tables.html")

def charts(request):
    return render(request, "charts.html")

def favorite(request):
    return render(request, "favorite.html")

def contact(request):
    return render(request, "contact.html")