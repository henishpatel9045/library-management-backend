# Generated by Django 4.2.5 on 2023-09-20 05:02

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="image",
            field=models.ImageField(null=True, upload_to=core.models.upload_book),
        ),
    ]