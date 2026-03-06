from django import forms
from .models import Event, Participant, Category

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
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple,  
        required=False
    )

    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'events': forms.SelectMultiple(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'description': forms.Textarea(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
        }