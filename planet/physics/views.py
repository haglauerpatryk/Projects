import numpy as np

from django.shortcuts import render
from django.views import View

# Create your views here.

class Index(View):
    title = "Physics"
    template_name = "index.html"

    def get(self, request):
        if request.method == "GET":
            return render(request, self.template_name, {"title": self.title})
        

class Physics():
    r"""
    For the naming of the methods 
    I'll use names of the laws of physics.

    For the naming of the variables I'll use
    the names of the variables in the laws 
    of physics and corresponding letters.
    """

    def newton_first_law(self, variable):
        pass
    
