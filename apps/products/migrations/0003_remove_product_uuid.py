# Generated by Django 3.2.20 on 2023-09-01 20:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_auto_20230902_0540"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="uuid",
        ),
    ]
