from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .forms import SignUpForm, XMLUploadForm
from .models import User, JobSeeker, Employer, Job
import xml.etree.ElementTree as ET
from django.db.models import Q  # Import Q for complex queries
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from .decorators import admin_required


def home(request):
    return render(request, 'UserApp/home.html')  

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('custom_login')  
    template_name = 'UserApp/signup.html'  

@admin_required
def admin_dashboard(request):
    employers = Employer.objects.all()
    return render(request, 'UserApp/admin_dashboard.html', {'employers': employers})

def handle_uploaded_xml(xml_file, employer):
    tree = ET.ElementTree(ET.fromstring(xml_file.read()))
    root = tree.getroot()
    
    for job_elem in root.findall('job'):
        apply_url = job_elem.find('applyURL')
        if apply_url is not None:  # This checks that the applyURL element was found in the XML
            apply_url = apply_url.text

        Job.objects.create(
            employer=employer,
            job_title=job_elem.find('jobTitle').text,
            location=job_elem.find('location').text,
            job_description=job_elem.find('jobDescription').text,
            apply_url=apply_url,  # Save the apply_url to the new job
        )

def upload_xml(request):
    if request.method == 'POST':
        form = XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            employer = form.cleaned_data['employer']
            xml_file = request.FILES['xml_file']
            handle_uploaded_xml(xml_file, employer)
            return redirect('admin_dashboard')
    else:
        form = XMLUploadForm()
    return render(request, 'UserApp/upload_xml.html', {'form': form})

class JobListView(ListView):
    model = Job
    template_name = 'UserApp/job_list.html'

    def get_queryset(self):
        db_jobs = super().get_queryset()
        # Integrate XML jobs once the function to parse XML jobs is implemented
        return db_jobs  

def parse_xml_jobs():
    # To be implemented: XML parsing logic
    pass

class JobDetailView(DetailView):
    model = Job
    template_name = 'UserApp/job_detail.html'

class JobListXMLView(TemplateView):
    content_type = 'application/xml'  # This sets the correct content type
    template_name = 'UserApp/job_list_xml.xml'  # This should point to your new XML template

    def get(self, request, *args, **kwargs):
        jobs = Job.objects.all()
        context = {'jobs': jobs}
        return self.render_to_response(context)

class DashboardView(TemplateView):
    template_name = "UserApp/dashboard.html"

class LoginView(AuthLoginView):
    template_name = 'UserApp/login.html'
    model = User
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard') 
