from django.contrib import admin
from .models import User, Employer, JobSeeker, Job, Analytics

admin.site.register(User)
admin.site.register(Employer)
admin.site.register(JobSeeker)
admin.site.register(Job)
admin.site.register(Analytics)
