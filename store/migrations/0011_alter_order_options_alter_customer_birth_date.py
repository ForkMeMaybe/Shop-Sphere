# Generated by Django 5.1.4 on 2024-12-13 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0010_alter_customer_options_remove_customer_email_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"permissions": [("cancel_order", "Can cancel order")]},
        ),
        migrations.AlterField(
            model_name="customer",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
