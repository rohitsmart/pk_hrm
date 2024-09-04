from django.db import models
from user.models import User
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



class department(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)

class project(models.Model):
    id=models.AutoField(primary_key= True)
    dId=models.ForeignKey(department,on_delete=models.CASCADE)
    name=models.CharField(max_length=60)
    startDate=models.DateField()
    endDate=models.DateField()
    requiredSkills=models.TextField()

class employee_project(models.Model):
    id=models.AutoField(primary_key=True)
    empId=models.ForeignKey(User,on_delete=models.CASCADE)
    pId=models.ForeignKey(project,on_delete=models.CASCADE)
    role=models.CharField(max_length=40)
    hoursWorked=models.CharField(max_length=30)

class leave(models.Model):
    id=models.AutoField(primary_key=True)
    Type=[("PL","PRIVILEDGED_LEAVE"),
        ("SL","SICK_LEAVE"),
        ("CL","CASUAL_LEAVE"),
        ("ML","MATERNITY_LEAVE"),]
    leaveType=models.CharField(max_length=30,choices=Type)
    description=models.TextField()

class Employee_Leave(models.Model):
    id=models.AutoField(primary_key=True)
    empId=models.ForeignKey(User,on_delete=models.CASCADE)
    Lid=models.ForeignKey(leave,on_delete=models.CASCADE)
    StartDate=models.DateField()
    endDate=models.DateField()
    status_choices=[('accepted','Accepted'),
                      ('rejected','Rejected'),
                       ('pending','Pending')]
    status=models.CharField(max_length=40,choices=status_choices)

class salary(models.Model):
    id=models.AutoField(primary_key=True)
    empId=models.ForeignKey(User,on_delete=models.CASCADE)
    basic_salary=models.CharField(max_length=50)
    allowance=models.CharField(max_length=50)
    deductions=models.CharField(max_length=50)
    net_sal=models.CharField(max_length=50)

class JobOpenings(models.Model):
    id=models.AutoField(primary_key=True)
    description=models.TextField()
    Totalvacancies=models.IntegerField()
    requiredSkills=models.CharField(max_length=60)
    filledvacancies=models.IntegerField()
