from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .models import Event
from django.contrib.auth import get_user_model


User = get_user_model()

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
            
            user = User.objects.get(id=user_id)
            
            send_mail(
                "RSVP Confirmation",
                
                f"You have successfully RSVP'd for the event: {instance.name}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )

