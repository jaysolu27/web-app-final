# Generated by Django 4.1.7 on 2023-03-14 20:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("apiApp", "0011_alter_productmodel_date_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productmodel",
            name="date_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
