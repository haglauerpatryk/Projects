from django.contrib import admin
from .models import Contact, DailyStockData

# Register your models here.

admin.site.register(DailyStockData)
admin.site.register(Contact)