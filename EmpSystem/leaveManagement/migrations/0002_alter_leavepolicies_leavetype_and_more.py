# Generated by Django 5.0.7 on 2024-09-12 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaveManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavepolicies',
            name='leaveType',
            field=models.CharField(choices=[('casualLeave', 'CL'), ('maternityLeave', 'ML'), ('earnedLeave', 'EL'), ('sickLeave', 'SL')], max_length=40, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='status',
            field=models.CharField(choices=[('rejected', 'rejected'), ('pending', 'pending'), ('allowed', 'allowed')], max_length=50),
        ),
    ]
