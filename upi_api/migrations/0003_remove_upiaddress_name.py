# Generated by Django 4.2.3 on 2023-07-27 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("upi_api", "0002_upiaddress_name"),
    ]

    operations = [
        migrations.RemoveField(model_name="upiaddress", name="name",),
    ]
