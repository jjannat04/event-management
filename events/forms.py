from django import forms
from .models import Event, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


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



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'profile_image': forms.FileInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
        }

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('phone_number', 'profile_image', 'email', 'first_name', 'last_name')        