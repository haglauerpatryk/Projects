# Generated by Django 5.0.1 on 2024-02-24 04:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_rename_close_stock_close_stock_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="DailyStockData",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("daily_open", models.DecimalField(decimal_places=2, max_digits=10)),
                ("daily_high", models.DecimalField(decimal_places=2, max_digits=10)),
                ("daily_low", models.DecimalField(decimal_places=2, max_digits=10)),
                ("daily_close", models.DecimalField(decimal_places=2, max_digits=10)),
                ("daily_volume", models.BigIntegerField()),
                ("daily_return", models.DecimalField(decimal_places=6, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="MonthlyStockData",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("year", models.PositiveIntegerField()),
                ("month", models.PositiveSmallIntegerField()),
                ("monthly_open", models.DecimalField(decimal_places=2, max_digits=10)),
                ("monthly_high", models.DecimalField(decimal_places=2, max_digits=10)),
                ("monthly_low", models.DecimalField(decimal_places=2, max_digits=10)),
                ("monthly_close", models.DecimalField(decimal_places=2, max_digits=10)),
                ("monthly_volume", models.BigIntegerField()),
                (
                    "monthly_return",
                    models.DecimalField(decimal_places=6, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ticker",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("ticker", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="YearlyStockData",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("year", models.PositiveIntegerField()),
                ("yearly_open", models.DecimalField(decimal_places=2, max_digits=10)),
                ("yearly_high", models.DecimalField(decimal_places=2, max_digits=10)),
                ("yearly_low", models.DecimalField(decimal_places=2, max_digits=10)),
                ("yearly_close", models.DecimalField(decimal_places=2, max_digits=10)),
                ("yearly_volume", models.BigIntegerField()),
                ("yearly_return", models.DecimalField(decimal_places=6, max_digits=10)),
                (
                    "ticker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.ticker"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Stock",
        ),
        migrations.AddField(
            model_name="monthlystockdata",
            name="ticker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.ticker"
            ),
        ),
        migrations.AddField(
            model_name="dailystockdata",
            name="ticker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.ticker"
            ),
        ),
    ]