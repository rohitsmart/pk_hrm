# Generated by Django 5.0.7 on 2024-09-12 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_profile_empid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilecounter',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
