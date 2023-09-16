from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView
from .forms import SignUpForm, XMLUploadForm
from .models import User, JobSeeker, Employer, Job
import xml.etree.ElementTree as ET
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
    success_url = reverse_lazy('UserApp:login')  # Updated to use 'UserApp' namespace
    template_name = 'UserApp/signup.html'

@admin_required
def admin_dashboard(request):
    employers = Employer.objects.all()
    return render(request, 'UserApp/admin_dashboard.html', {'employers': employers})

def parse_xml_jobs(xml_file, employer):
    # TODO: Implement the XML parse logic
    pass

def upload_xml(request):
    if request.method == 'POST':
        form = XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['xml_file']
            selected_employer = form.cleaned_data['employer']
            
            # Parse the XML file and create job listings
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for job_node in root.findall('job'):
                # Create a job associated with the selected employer
                Job.objects.create(
                    title=job_node.findtext('title'),
                    description=job_node.findtext('description'),
                    employer=selected_employer,
                    location=job_node.findtext('location'),
                    date_posted=job_node.findtext('datePosted'),
                    promoted=job_node.findtext('promoted') == 'true',
                    apply_url=job_node.findtext('applyUrl'),
                    salary=job_node.findtext('salary'),
                    job_type=job_node.findtext('jobType'),
                    job_id=job_node.findtext('jobId'),  # Adding job_id
                )
            
            return redirect('/jobs')
    else:
        form = XMLUploadForm(user=request.user)

    return render(request, 'UserApp/upload_xml.html', {'form': form})

class JobListView(ListView):
    model = Job
    template_name = "UserApp/job_list.html"

class JobDetailView(DetailView):
    model = Job
    template_name = "UserApp/job_detail.html"

class JobListXMLView(ListView):
    model = Job
    template_name = 'UserApp/job_list_xml.xml'
    
    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/xml'
        return super().render_to_response(context, **response_kwargs)

class DashboardView(TemplateView):
    template_name = "UserApp/dashboard.html"

class LoginView(AuthLoginView):
    template_name = 'UserApp/login.html'

    def get_success_url(self):
        return reverse_lazy('UserApp:dashboard')
