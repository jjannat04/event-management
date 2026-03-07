from django import forms
from .models import Event, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


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






class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'e.g. +88017...'}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile.save()
        return profile

        