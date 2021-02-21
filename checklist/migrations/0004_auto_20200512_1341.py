# Generated by Django 3.0.4 on 2020-05-12 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("checklist", "0003_checklist_upvotes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="checklist",
            name="upvotes",
        ),
        migrations.CreateModel(
            name="Upvotes",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "checklist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="checklist.Checklist",
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
        ),
    ]
