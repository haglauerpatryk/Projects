from django.shortcuts import render
from .models import Stock, Contact
from django.contrib import messages
from django.views import View


"""
Showcase of the structure of the views.py file

BaseView:
    IndexView
    ContactView
    StockView:
        TablesView
        ChartsView
        FavouriteView

"""

class BaseView(View):
    title = None
    template_name = None

    def get(self, request):
        return render(request, self.template_name, {"title": self.title})
    

class IndexView(BaseView):
    title = "Dashboard"
    template_name = "index.html"

class ContactView(BaseView):
    title = "Contact"
    template_name = "contact.html"

    def post(self, request):
        if request.method != "POST":
            return render(request, "contact.html", {"title": self.title})
        
        name    = request.POST.get("name")
        email   = request.POST.get("email")
        message = request.POST.get("message")
        pnumber = request.POST.get("pnumber")

        query = Contact(name=name, email=email, message=message, pnumber=pnumber)
        query.save()
        messages.info(request, "Your message has been sent successfully!")
        return render(request, "contact.html", {"title": self.title})
    

class StockView(BaseView):

    def post(self, request):
        if request.method != "POST":
            return render(request, "index.html", {"title": self.title})

        ticker = request.POST.get("ticker")
        date   = request.POST.get("date")
        open   = request.POST.get("open")
        high   = request.POST.get("high")
        low    = request.POST.get("low")
        close  = request.POST.get("close")
        volume = request.POST.get("volume")

        query = Stock(ticker=ticker, date=date, open=open, high=high, low=low, close=close, volume=volume)
        query.save()
        messages.info(request, "Your stock has been saved successfully!")
        return render(request, "index.html", {"title": self.title})

class TablesView(StockView):
    title = "Tables"
    template_name = "tables.html"


class ChartsView(StockView):
    title = "Charts"
    template_name = "charts.html"


class FavouriteView(StockView):
    title = "Favourite"
    template_name = "favourite.html"