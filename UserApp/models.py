from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Your User class definition

class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer')
    # ... the rest of your fields and other model definitions

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('JS', 'Job Seeker'),
        ('EM', 'Employer'),
        ('AD', 'Admin'),
    )
    
    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES, default='JS')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="userapp_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="userapp_user_set",
        related_query_name="user",
    )

class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer')
    name = models.CharField(max_length=255)
    xml_feed = models.FileField(upload_to='xml_feeds/', null=True, blank=True)
    payment_details = models.CharField(max_length=255, null=True, blank=True)

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')
    location = models.CharField(max_length=255)
    date_posted = models.DateTimeField(auto_now_add=True)
    promoted = models.BooleanField(default=False)

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='job_seeker')
    bookmarked_jobs = models.ManyToManyField(Job, related_name='bookmarked_by')

class Analytics(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='analytics')
    clicks = models.IntegerField(default=0)
