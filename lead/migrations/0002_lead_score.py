# Generated by Django 5.1.7 on 2025-03-18 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='score',
            field=models.FloatField(default=0.0),
        ),
    ]
