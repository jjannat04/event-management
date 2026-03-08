from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile_images', 
        blank=True, 
        default='profile_images/default.png'
    )
    
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be between 9 and 15 digits."
    )
    phone_number = models.CharField(
        validators=[phone_validator], 
        max_length=17, 
        blank=True, 
        null=True
    )
    @property
    def is_admin(self):
        return self.groups.filter(name='Admin').exists()

    @property
    def is_organizer(self):
        return self.groups.filter(name='Organizer').exists()
    
    @property
    def is_participant(self):
        return self.groups.filter(name='Participant').exists()
    
    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


from django.db import models
from django.conf import settings # Add this to get AUTH_USER_MODEL

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)

    category = models.ForeignKey(
        'Category', # Use string to avoid import order issues
        on_delete=models.CASCADE,
        related_name="events"
    )

    # CHANGE THIS: Use settings.AUTH_USER_MODEL instead of User
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events",
        null=True # Keep null=True temporarily to help with migrations
    )

    # CHANGE THIS: Use settings.AUTH_USER_MODEL here too
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='rsvped_events',
        blank=True
    )

    image = models.ImageField(
        upload_to="event_images/",
        default="event_images/default.jpeg"
    )

    def __str__(self):
        return self.name

#fix
#reset
