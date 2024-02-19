from django.db import models

# Create your models here.

class Stock(models.Model):
    
    ticker = models.CharField(max_length=10)
    date   = models.DateField()
    open   = models.FloatField()
    high   = models.FloatField()
    low    = models.FloatField()
    close  = models.FloatField()
    volume = models.FloatField()

    def __str__(self):
        return self.ticker
    

class Contact(models.Model):
    
    name    = models.CharField(max_length=200)
    email   = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name