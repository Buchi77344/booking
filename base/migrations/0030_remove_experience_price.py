# Generated by Django 5.0.1 on 2024-10-13 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_experience_max_guests_experience_min_guests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='price',
        ),
    ]
