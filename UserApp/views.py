from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import SignUpForm

# Other views can be here

class LoginView(TemplateView):
    template_name = "UserApp/login.html"
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Ensure you have a URL pattern named 'dashboard' in your urls.py file
        else:
            return render(request, self.template_name, {'error': 'Invalid username or password'})

class SignUpView(TemplateView):
    template_name = "UserApp/signup.html"
    
    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signing up
            return redirect('dashboard')  # Ensure you have a URL pattern named 'dashboard' in your urls.py file
        else:
            return render(request, self.template_name, {'form': form, 'error': 'There were one or more errors in your form.'})

class DashboardView(TemplateView):
    template_name = "UserApp/dashboard.html"

def home(request):
    return render(request, 'UserApp/home.html')
