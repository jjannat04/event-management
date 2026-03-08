from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Event, Category, CustomUser # Removed UserProfile

# 1. Register Regular Models
admin.site.register(Event)
admin.site.register(Category)

# 2. Register CustomUser with the special UserAdmin interface
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # This adds your new fields to the "User Change" page in Admin
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Profile Info', {'fields': ('profile_image', 'phone_number')}),
    )
    
    # This adds your new fields to the "Add User" page in Admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Profile Info', {'fields': ('profile_image', 'phone_number')}),
    )

    # These columns will show up in the main User list table
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff']
    search_fields = ['username', 'email', 'phone_number']