# Generated by Django 5.0.1 on 2024-02-24 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_dailystockdata_monthlystockdata_ticker_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticker",
            name="market",
            field=models.CharField(default=None, max_length=10),
        ),
    ]
