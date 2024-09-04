from django.db import models
class User(models.Model):
   username=models.CharField(max_length=50)
   email=models.EmailField(unique=True,null=True)
   password=models.TextField()
   role=models.CharField(max_length=20,null= True,default='employee')
   