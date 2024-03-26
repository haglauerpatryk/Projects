from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View

class ViewConfig(View):
    title = None
    template_name = None

class RegisterView(ViewConfig):
    title = "Register"
    template_name = "authentication/register.html"

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
            
    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

class LoginView(ViewConfig):
    title = "Login"
    template_name = "authentication/login.html"

    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
                

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})
