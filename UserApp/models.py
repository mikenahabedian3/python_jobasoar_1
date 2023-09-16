from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _



class JobListing(models.Model):
    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_description = models.TextField()
    apply_url = models.URLField()

    def __str__(self):
        return self.job_title


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

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
    
    objects = CustomUserManager()

class Employer(models.Model):
    name = models.CharField(max_length=255)
    xml_feed = models.FileField(upload_to='xml_feeds/', null=True, blank=True)
    payment_details = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name


class Job(models.Model):
    # Choices for the job_type field
    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        # Add other job types as needed
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')
    location = models.CharField(max_length=255)
    date_posted = models.DateTimeField(auto_now_add=True)
    promoted = models.BooleanField(default=False)
    apply_url = models.URLField(null=True, blank=True)  # Allow the field to be nullable and blank in forms

    salary = models.CharField(max_length=255, null=True, blank=True)  # Store salary information, if available
    job_type = models.CharField(max_length=50, null=True, blank=True, choices=JOB_TYPE_CHOICES)  # Store the job type, if available

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='job_seeker')
    bookmarked_jobs = models.ManyToManyField(Job, related_name='bookmarked_by')

class Analytics(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='analytics')
    clicks = models.IntegerField(default=0)
