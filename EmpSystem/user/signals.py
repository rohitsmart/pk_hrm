from django.db.models.signals import post_migrate
from django.dispatch import receiver
from user.models import User 
from django.contrib.auth.hashers import make_password


@receiver(post_migrate)
def create_entry(sender, **kwargs):
    
  if not User.objects.filter(username="admin").exists():
     User.objects.create(username="admin",password=make_password("admin@123"),role="admin",email='admin@gmail.com')