from django.db import models

# Create your models here.

class Stock(models.Model):
    
    id     = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10)
    date   = models.DateField()
    open_stock   = models.FloatField()
    high_stock   = models.FloatField()
    low_stock    = models.FloatField()
    close_stock  = models.FloatField()
    volume = models.FloatField()

    def __str__(self):
        return self.ticker
    

class Contact(models.Model):
    
    name    = models.CharField(max_length=200)
    email   = models.EmailField()
    message = models.TextField()
    pnumber = models.CharField(max_length=20)

    def __str__(self):
        return self.name