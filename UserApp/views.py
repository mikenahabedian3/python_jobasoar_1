from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView  
from .forms import SignUpForm, XMLUploadForm
from .models import User, JobSeeker, Employer, Job
import xml.etree.ElementTree as ET
from django.db.models import Q
from django.contrib.auth.views import LoginView as AuthLoginView 
from django.urls import reverse_lazy
from .decorators import admin_required
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'UserApp/home.html'

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('custom_login')
    template_name = 'UserApp/signup.html'

@admin_required
def admin_dashboard(request):
    employers = Employer.objects.all()
    return render(request, 'UserApp/admin_dashboard.html', {'employers': employers})

def parse_xml_jobs(xml_file, employer):
    # parse xml logic
    pass

def upload_xml(request):
    # upload xml logic 
    pass

class JobListView(ListView):
    # JobListView logic
    pass

class JobDetailView(DetailView):
    # JobDetailView logic
    pass

class JobListXMLView(TemplateView):
    # JobListXMLView logic
    pass

class DashboardView(TemplateView):
    # DashboardView logic
    pass

class LoginView(AuthLoginView):
    template_name = 'UserApp/login.html'  # Specify the correct path to your login template
    success_url = reverse_lazy('UserApp:dashboard')  # Assuming you have a URL pattern named 'dashboard' in your UserApp's urls.py
