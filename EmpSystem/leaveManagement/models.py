from django.db import models
from user.models import ProfileCounter
class leavePolicies(models.Model):
    Type={
        ('sickLeave','SL'),
        ('maternityLeave','ML'),
        ('casualLeave','CL'),
        ('earnedLeave','EL'),
    }
    leaveType=models.CharField(max_length=40,choices=Type,unique=True,primary_key=True)
    description=models.TextField()
    CarryOverLimit=models.CharField(max_length=6)
    payoutPolicy=models.TextField()


class leaveRequest(models.Model):
   type={
       ('pending','pending'),
       ('allowed','allowed'),
       ('rejected','rejected')
   }
   id=models.AutoField(primary_key=True)
   empId=models.ForeignKey(ProfileCounter,on_delete=models.CASCADE)
   leaveType=models.ForeignKey(leavePolicies,on_delete=models.CASCADE)
   startDate=models.DateField()
   endDate=models.DateField()
   duration=models.CharField(max_length=30)
   status=models.CharField(max_length=50,choices=type)
   description=models.TextField()
   time=models.TimeField()
   approvedBy=models.CharField(max_length=40,null=True)
   approvaldate=models.DateField(null=True)
   approvalTime=models.TimeField(null=True)
   

