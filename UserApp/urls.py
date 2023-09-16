from django.urls import path, include
from .views import HomeView, SignUpView, DashboardView, LoginView, admin_dashboard, upload_xml, JobListView, JobDetailView, JobListXMLView  
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'UserApp'  # Updated to 'UserApp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('login/', LoginView.as_view(), name='login'), 
    path('signup/', SignUpView.as_view(), name='signup'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('upload-xml/', upload_xml, name='upload_xml'),
    path('jobs/', JobListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('job-list-xml/', JobListXMLView.as_view(), name='job_list_xml'),
    path('logout/', LogoutView.as_view(next_page='UserApp:home'), name='logout'),  # Updated to use 'UserApp' namespace
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
