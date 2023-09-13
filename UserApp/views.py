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

# Need a home page 
def home(request):
    # Your existing code for rendering the landing page goes here
    return render(request, 'UserApp/home.html')  # Adjust the template path as needed

# Sign Up view (existing)
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('custom_login')  # Update with the correct login URL name
    template_name = 'UserApp/signup.html'  # Ensure this matches the template name

# Admin Dashboard view with decorator (existing)
@admin_required
def admin_dashboard(request):
    # Your admin dashboard view logic here
    # Get a list of all employers
    employers = Employer.objects.all()
    return render(request, 'UserApp/admin_dashboard.html', {'employers': employers})

# New code for handling uploaded XML files
def handle_uploaded_xml(xml_file, employer):
    tree = ET.ElementTree(ET.fromstring(xml_file.read()))
    root = tree.getroot()

    for job_elem in root.findall('job'):
        job = Job.objects.create(
            employer=employer,
            job_title=job_elem.find('jobTitle').text,
            location=job_elem.find('location').text,
            job_description=job_elem.find('jobDescription').text,
            # Add other job fields as needed
        )

# XML Upload view
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

# Modify JobListView to include XML data (existing)
class JobListView(ListView):
    model = Job
    template_name = 'UserApp/job_list.html'

    def get_queryset(self):
        # Fetch jobs from the database
        db_jobs = super().get_queryset()

        # Fetch jobs from XML files (you'll need a function to parse and retrieve jobs from XML)
        xml_jobs = parse_xml_jobs()  # Implement this function

        # Combine the two sets of jobs
        all_jobs = db_jobs | xml_jobs

        return all_jobs

# New code snippet for parsing XML jobs (existing)
def parse_xml_jobs():
    # Implement XML parsing logic to extract jobs from uploaded XML files
    # Create Job objects based on the XML data
    # Return a queryset of jobs from XML data
    pass

# Job Detail view (existing)
class JobDetailView(DetailView):
    model = Job
    template_name = 'UserApp/job_detail.html'

# XML Job List view (existing)
class JobListXMLView(TemplateView):
    content_type = 'text/xml'
    template_name = 'UserApp/job_list_xml.xml'

    def get(self, request, *args, **kwargs):
        # Get all jobs
        jobs = Job.objects.all()
        context = {'jobs': jobs}
        return self.render_to_response(context)

# DashboardView (existing)
class DashboardView(TemplateView):
    template_name = "UserApp/dashboard.html"


# Custom Login view (existing)
class LoginView(AuthLoginView):
    template_name = 'UserApp/login.html'  # Specify the correct template path

    # Specify the User model as the queryset
    model = User
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')  # Update with your success URL

