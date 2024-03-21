from django.db import models

# Create your models here.

class DailyStockData(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    daily_open = models.DecimalField(max_digits=10, decimal_places=4)
    daily_high = models.DecimalField(max_digits=10, decimal_places=4)
    daily_low  = models.DecimalField(max_digits=10, decimal_places=4)
    daily_close  = models.DecimalField(max_digits=10, decimal_places=4)
    daily_volume = models.DecimalField(max_digits=18, decimal_places=4)

    def __str__(self):
        return self.ticker
    
class Contact(models.Model):
    
    name    = models.CharField(max_length=200)
    email   = models.EmailField()
    message = models.TextField()
    pnumber = models.CharField(max_length=20)

    def __str__(self):
        return self.name