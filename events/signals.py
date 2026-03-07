from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Event
from .models import UserProfile


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):

    if created and not instance.is_active:

        token = default_token_generator.make_token(instance)

        activation_link = f"http://127.0.0.1:8000/events/activate/{instance.id}/{token}/"

        send_mail(
            "Activate your account",
            f"Activate your account using this link:\n{activation_link}",
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=True,
        )




@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_email(sender, instance, action, pk_set, **kwargs):

    if action == "post_add":

        for user_id in pk_set:

            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)

            send_mail(
                "RSVP Confirmation",
                f"You have successfully RSVP'd for the event: {instance.name}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )        



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()     

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)           