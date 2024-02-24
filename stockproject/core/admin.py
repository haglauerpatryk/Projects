from django.contrib import admin
from .models import Contact, DailyStockData, MonthlyStockData, YearlyStockData

# Register your models here.

admin.site.register(DailyStockData)
admin.site.register(MonthlyStockData)
admin.site.register(YearlyStockData)
admin.site.register(Contact)