from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()

    date = models.DateField()
    time = models.TimeField()

    location = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events"
    )

    participants = models.ManyToManyField(
        User,
        related_name='rsvped_events',
        blank=True
    )

    image = models.ImageField(
        upload_to="event_images/",
        default="event_images/default.jpeg"
    )

    def __str__(self):
        return self.name
    

    from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', blank=True)
    
    # This validator ensures the number is not just 3 digits
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{11}$',
        message="Phone number must be of 11 digits."
    )
    phone_number = models.CharField(validators=[phone_validator], max_length=17, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"