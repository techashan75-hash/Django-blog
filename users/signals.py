from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from .utils import send_welcome_email

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
  if created:
    #logic to be triggered
    Profile.objects.create(user=instance)
   
@receiver(post_save, sender=User)  
def save_profile(sender,instance,**kwargs):
  instance.profile.save()
  
@receiver(post_save,sender=User) 
def send_welcome_confirm_email(sender,created,instance,**kwargs):
  if created:
    send_welcome_email(instance)