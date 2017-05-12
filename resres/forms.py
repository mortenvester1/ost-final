from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required = True, help_text = 'email',widget=forms.TextInput(attrs={'placeholder': 'ex: name@example.com'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ResourceForm(forms.Form):
    name = forms.CharField(max_length=100, label='Resource Name', help_text='ex: Tabels',widget=forms.TextInput(attrs={'placeholder': 'ex: Tuba'}))
    tags = forms.CharField(max_length=100, label='Tags', help_text='ex: Party Guest Tuba',widget=forms.TextInput(attrs={'placeholder': 'ex: Music Instrument'}))
    #start = forms.CharField(max_length=100, label='Avail Start')
    #end = forms.CharField(max_length=100, label='Avail End')
    start = forms.TimeField(input_formats=['%H:%M'], help_text='ex: 10:30', label = 'Avail Start',widget=forms.TextInput(attrs={'placeholder': 'ex: 10:30'}))
    end = forms.TimeField(input_formats=['%H:%M'], help_text='ex: 21:30', label = 'Avail End',widget=forms.TextInput(attrs={'placeholder': 'ex: 21:30'}))
    
class ReservationForm(forms.Form):
    #date = forms.CharField(max_length=100, label='Date', help_text='ex: DD/MM/YY',widget=forms.TextInput(attrs={'placeholder': 'ex: 27/12/17'}))
    #start = forms.CharField(max_length=100, label='Start Time')
    #duration = forms.CharField(max_length=100, label='End Time')
    date = forms.DateField(input_formats=['%d/%m/%Y'],label='Date', help_text='ex: DD/MM/YY',widget=forms.TextInput(attrs={'placeholder': 'ex: 27/12/2017'}))
    start = forms.TimeField(input_formats=['%H:%M'], help_text='ex: 10:30', label='Start Time',widget=forms.TextInput(attrs={'placeholder': 'ex: 10:30'}))
    duration = forms.CharField(max_length=100, help_text='ex: 2:30', label = 'Duration',widget=forms.TextInput(attrs={'placeholder': 'ex: 1:45'}))
