# Generated by Django 3.2.21 on 2023-09-16 13:16

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_category_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="optiongroup",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]