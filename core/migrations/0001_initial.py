# Generated by Django 4.2.5 on 2023-09-20 04:58

import core.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(max_length=255)),
                ("isbn", models.CharField(max_length=13, unique=True)),
                ("image", models.ImageField(upload_to=core.models.upload_book)),
            ],
        ),
        migrations.CreateModel(
            name="BookCopy",
            fields=[
                (
                    "barcode",
                    models.CharField(
                        max_length=20, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("is_available", models.BooleanField(default=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.book"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IssueRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("request_date", models.DateTimeField(auto_now_add=True)),
                ("is_approved", models.BooleanField(default=False)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.book"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-request_date"],
            },
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("issue_date", models.DateField()),
                ("due_date", models.DateField()),
                ("return_date", models.DateField(blank=True, null=True)),
                (
                    "penalty_amount",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(
                                0, "Penalty amount can't be negative."
                            )
                        ],
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.bookcopy"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-issue_date", "-return_date"],
            },
        ),
    ]