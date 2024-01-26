from django.db import models
from users.models import User
from stocks.models import StockData

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(StockData, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)  # 'buy' or 'sell'
    transaction_volume = models.IntegerField()
    transaction_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


     

