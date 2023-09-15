from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Employer

class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True, help_text='Select your user type', widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type')

class XMLUploadForm(forms.Form):
    xml_file = forms.FileField(label='Upload XML File')
    employer = forms.ModelChoiceField(queryset=Employer.objects.all(), required=True, help_text='Select the employer')
