from django.shortcuts import render, redirect
from .models import Stock, Contact
from django.contrib import messages
from django.views import View
from .forms import StockForm

"""
Showcase of the structure of the views.py file
ViewConfig:
    BaseTemplateView:
        IndexView
        ContactView

    StockTemplateView:
        TablesView
        ChartsView
        FavouriteView

"""

class ViewConfig(View):
    title = None
    template_name = None

class BaseTemplateView(ViewConfig):

    def get(self, request):
        return render(request, self.template_name, {"title": self.title})
    

class IndexView(BaseTemplateView):
    title = "Dashboard"
    template_name = "index.html"

class ContactView(BaseTemplateView):
    title = "Contact"
    template_name = "contact.html"

    def post(self, request):
        if request.method != "POST":
            return render(request, "contact.html", {"title": self.title})
        
        name    = request.POST.get("name")
        email   = request.POST.get("email")
        message = request.POST.get("message")
        pnumber = request.POST.get("pnumber")

        query = Contact(
            name=name, 
            email=email, 
            message=message, 
            pnumber=pnumber
        )
        query.save()
        messages.info(request, "Your message has been sent successfully!")
        return render(request, "contact.html", {"title": self.title})
    

class StockTemplateView(ViewConfig):

    def get(self, request):
        if request.method != "GET":
            return render(request, self.template_name, {"title": self.title})

        stocks = Stock.objects.all()

        return render(request, self.template_name, {"stocks": stocks, "title": self.title})

class TablesView(StockTemplateView):
    title = "Tables"
    template_name = "tables.html"


class ChartsView(StockTemplateView):
    title = "Charts"
    template_name = "charts.html"


class FavouriteView(StockTemplateView):
    title = "Favourite"
    template_name = "favourite.html"