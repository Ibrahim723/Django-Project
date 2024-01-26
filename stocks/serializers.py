from rest_framework import serializers
from .models import StockData

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['ticker', 'open_price', 'close_price', 'high', 'low', 'volume', 'timestamp']
