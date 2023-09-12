from django.urls import path
from .views import DashboardView, LoginView, SignUpView, home, JobListView, JobDetailView  # Import all the necessary views

urlpatterns = [
    # Home URL - the landing page when users visit your site
    path('', home, name='home'),  

    # Dashboard URL - where users are redirected after successful login/signup
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  
    
    # Login URL - where users can log in to their accounts
    path('login/', LoginView.as_view(), name='custom_login'),  
    
    # Sign up URL - where new users can create accounts
    path('signup/', SignUpView.as_view(), name='signup'),  

    # Job listing and detail URLs - where users can view job listings and details
    path('jobs/', JobListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
]