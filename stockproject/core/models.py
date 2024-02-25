from django.db import models

# Create your models here.

class Ticker(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10, unique=True)
    market = models.CharField(max_length=10, default=None)

    def __str__(self):
        return self.ticker

class DailyStockData(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    date = models.DateField()
    daily_open = models.DecimalField(max_digits=10, decimal_places=4)
    daily_high = models.DecimalField(max_digits=10, decimal_places=4)
    daily_low  = models.DecimalField(max_digits=10, decimal_places=4)
    daily_close  = models.DecimalField(max_digits=10, decimal_places=4)
    daily_volume = models.BigIntegerField()
    daily_return = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)

    def __str__(self):
        return self.ticker

class MonthlyStockData(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    year  = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField()
    monthly_open = models.DecimalField(max_digits=10, decimal_places=4)
    monthly_high = models.DecimalField(max_digits=10, decimal_places=4)
    monthly_low  = models.DecimalField(max_digits=10, decimal_places=4)
    monthly_close  = models.DecimalField(max_digits=10, decimal_places=4)
    monthly_volume = models.BigIntegerField()
    monthly_return = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)

    def __str__(self):
        return self.ticker

class YearlyStockData(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    yearly_open = models.DecimalField(max_digits=10, decimal_places=4)
    yearly_high = models.DecimalField(max_digits=10, decimal_places=4)
    yearly_low  = models.DecimalField(max_digits=10, decimal_places=4)
    yearly_close  = models.DecimalField(max_digits=10, decimal_places=4)
    yearly_volume = models.BigIntegerField()
    yearly_return = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)

    def __str__(self):
        return self.ticker
    
class Contact(models.Model):
    
    name    = models.CharField(max_length=200)
    email   = models.EmailField()
    message = models.TextField()
    pnumber = models.CharField(max_length=20)

    def __str__(self):
        return self.name