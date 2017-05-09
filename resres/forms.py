from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required = True, help_text = 'email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ResourceForm(forms.Form):
    name = forms.CharField(max_length=100, label='Resource Name')
    tags = forms.CharField(max_length=100, label='Tags')
    start = forms.CharField(max_length=100, label='Avail Start')
    end = forms.CharField(max_length=100, label='Avail End')
    
class ReservationForm(forms.Form):
    date = forms.CharField(max_length=100, label='Date')
    start = forms.CharField(max_length=100, label='Start Time')
    end = forms.CharField(max_length=100, label='End Time')