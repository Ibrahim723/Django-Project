from django.db import models

class StockData(models.Model):
    ticker = models.CharField(max_length=255, primary_key=True)
    open_price = models.FloatField()
    close_price = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.IntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.ticker
