# Generated by Django 5.0.7 on 2024-09-12 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_profile_empcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='empCode',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='id',
        ),
        migrations.AlterField(
            model_name='profile',
            name='empid',
            field=models.IntegerField(default=1000, primary_key=True, serialize=False, unique=True),
        ),
    ]
