from django.shortcuts import render
from .models import Stock, Contact
from django.contrib import messages


# Create your views here.

def index(request):
    title = "Dashboard"

    return render(request, "index.html", {"title": title})

def tables(request):
    title = "Tables"

    return render(request, "tables.html", {"title": title})

def charts(request):
    title = "Charts"

    return render(request, "charts.html", {"title": title})

def favourite(request):
    title = "Favourite"

    return render(request, "favourite.html", {"title": title})

def contact(request):
    title = "Contact"

    if request.method == "POST":

        name    = request.POST.get("name")
        email   = request.POST.get("email")
        message = request.POST.get("message")
        pnumber = request.POST.get("pnumber")

        query = Contact(name=name, email=email, message=message, pnumber=pnumber)
        query.save()
        messages.info(request, "Your message has been sent successfully!")
        return render(request, "contact.html", {"title": title})

    return render(request, "contact.html", {"title": title})