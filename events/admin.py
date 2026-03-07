from django.contrib import admin
from .models import Event, Category
from .models import UserProfile

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(UserProfile)