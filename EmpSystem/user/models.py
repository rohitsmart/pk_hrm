from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, null=True, default='employee')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class profile(models.Model):
    userId=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    contact=models.CharField(max_length=15)
    designation=models.CharField(max_length=40)
    address=models.CharField(max_length=80)
    doj=models.DateField()
    salary=models.CharField(max_length=50)
    qualification=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    empid=models.IntegerField(unique=True,default=1000,primary_key=True)
class ProfileCounter(models.Model):
  
    EmpId=models.IntegerField(unique=True,primary_key= True,default=1000)    