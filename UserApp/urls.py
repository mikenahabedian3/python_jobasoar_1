from django.urls import path
from .views import DashboardView, LoginView, SignUpView, home  # Make sure to import your views

urlpatterns = [
    # Home URL - the landing page when users visit your site
    path('', home, name='home'),  

    # Dashboard URL - where users are redirected after successful login/signup
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  
    
    # Login URL - where users can log in to their accounts
    path('login/', LoginView.as_view(), name='custom_login'),  # Change was made here to get shit to work  
    
    # Sign up URL - where new users can create accounts
    path('signup/', SignUpView.as_view(), name='signup'),  
]
