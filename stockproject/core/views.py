from django.shortcuts import render
from .models import Stock, Contact
from django.contrib import messages
from django.views import View


# Create your views here.

class BaseView(View):
    title = None
    template_name = None

    def get(self, request):
        return render(request, self.template_name, {"title": self.title})
    

class IndexView(BaseView):
    title = "Dashboard"
    template_name = "index.html"


class TablesView(BaseView):
    title = "Tables"
    template_name = "tables.html"


class ChartsView(BaseView):
    title = "Charts"
    template_name = "charts.html"


class FavouriteView(BaseView):
    title = "Favourite"
    template_name = "favourite.html"


class ContactView(BaseView):
    title = "Contact"
    template_name = "contact.html"

    def post(self, request):
        if request.method == "POST":
            name    = request.POST.get("name")
            email   = request.POST.get("email")
            message = request.POST.get("message")
            pnumber = request.POST.get("pnumber")

            query = Contact(name=name, email=email, message=message, pnumber=pnumber)
            query.save()
            messages.info(request, "Your message has been sent successfully!")
            return render(request, "contact.html", {"title": self.title})