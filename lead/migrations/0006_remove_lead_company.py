# Generated by Django 5.1.7 on 2025-03-18 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0005_lead_engagement_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='company',
        ),
    ]
