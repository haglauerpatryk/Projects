# Generated by Django 5.0.1 on 2024-02-24 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_ticker_market"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailystockdata",
            name="daily_return",
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="monthlystockdata",
            name="monthly_return",
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="yearlystockdata",
            name="yearly_return",
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=10),
        ),
    ]
