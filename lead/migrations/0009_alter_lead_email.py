# Generated by Django 5.1.7 on 2025-03-18 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0008_lead_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
