from django.db.models.signals import post_migrate
from django.dispatch import receiver
from user.models import User,profile,ProfileCounter
from django.contrib.auth.hashers import make_password


@receiver(post_migrate)
def create_entry(sender, **kwargs):
    if not User.objects.filter(username="admin").exists():
        User.objects.create(
            username="admin",
            password=make_password("admin@123"),
            role="admin",
            email='admin@gmail.com'
        )
    
    if not profile.objects.filter(email="admin@gmail.com").exists():
        user=User.objects.get(email='admin@gmail.com')
        profile.objects.create(
            userId=user,
            name="abhi sharma",
            contact="123456789",
            designation='ceo',
            address='noida,up',
            doj='2020-01-01',
            salary='50,000',
            qualification='master in technology',
            email='admin@gmail.com'
        )

    if not ProfileCounter.objects.filter(EmpId=1000).exists():
            ProfileCounter.objects.create(
                 EmpId=1000
            )