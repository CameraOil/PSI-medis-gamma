# Generated by Django 5.2 on 2025-05-20 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodes',
            name='error_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
