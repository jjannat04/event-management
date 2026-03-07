from django import forms
from .models import Event, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'category', 'date', 'time', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'description': forms.Textarea(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'category': forms.Select(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'date': forms.DateInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
        }

class ParticipantForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'events']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'first_name': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'description': forms.Textarea(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
        }


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']