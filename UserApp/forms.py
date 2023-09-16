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
    # Remove the employer field since it's associated with the logged-in user

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the kwargs
        super(XMLUploadForm, self).__init__(*args, **kwargs)

        if user:
            # Filter the employers based on the logged-in user
            self.fields['employer'] = forms.ModelChoiceField(
                queryset=Employer.objects.filter(user=user),
                required=True,
                help_text='Select the employer'
            )
