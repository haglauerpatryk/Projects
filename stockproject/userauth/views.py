from django.shortcuts import render

# Create your views here.

def signup(request):
    return render(request, "userauth/signup.html")

def login(request):
    return render(request, "userauth/login.html")
