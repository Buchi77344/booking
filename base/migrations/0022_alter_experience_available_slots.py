# Generated by Django 5.0.1 on 2024-10-09 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_chatmessage_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='available_slots',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
