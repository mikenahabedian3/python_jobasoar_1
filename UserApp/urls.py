from django.urls import path
from . import views  # Import views from your app
from .views import LoginView
from django.contrib.auth.views import LogoutView



urlpatterns = [
    # Home URL - the landing page when users visit your site
    path('', views.home, name='home'),  

    # Dashboard URL - where users are redirected after successful login/signup
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),  
    
    # Login URL - where users can log in to their accounts
    path('login/', views.LoginView.as_view(), name='custom_login'),  
    
    # Sign up URL - where new users can create accounts
    path('signup/', views.SignUpView.as_view(), name='signup'),  
    
    # Admin Dashboard URL - for administrators
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # XML Upload URL - for uploading XML files
    path('upload-xml/', views.upload_xml, name='upload_xml'),
    
    # Job listing and detail URLs - where users can view job listings and details
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),

    # XML job listings URL - to generate XML response for job listings
    path('job-list-xml/', views.JobListXMLView.as_view(), name='job_list_xml'),
    
    # Logout URL - now users can log out once logged in
    path('logout/', LogoutView.as_view(), name='logout'),

]
