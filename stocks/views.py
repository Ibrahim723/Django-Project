from django.shortcuts import render, redirect
from django.views import View
from django.core.cache import cache
from datetime import datetime
from .models import StockData
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StockDataSerializer

class StockDataCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        ticker = request.data.get('ticker')
        open_price = float(request.data.get('open_price'))
        close_price = float(request.data.get('close_price'))
        high = float(request.data.get('high'))
        low = float(request.data.get('low'))
        volume = int(request.data.get('volume'))
        # Parse the timestamp string into a datetime object
        timestamp_str = request.data.get('timestamp')
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Create a new stock
        stock = StockData.objects.create(ticker=ticker, open_price=open_price, 
                                         close_price=close_price,high=high,low=low,
                                         volume=volume,timestamp=timestamp)

        # Serialize the user data
        serializer = StockDataSerializer(stock)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StockDataListView(generics.ListAPIView):
    queryset = StockData.objects.all()
    serializer_class = StockDataSerializer

    def get(self, request, *args, **kwargs):
        # Check if the entire list is in the cache
        cache_key = 'stock_data_list'
        stock_data_list = cache.get(cache_key)

        if stock_data_list is not None:
            # If the list is found in the cache, return it
            print("\n\n -------------- In cache -----------\n \n")
            return Response(stock_data_list, status=status.HTTP_200_OK)

        # If the list is not in the cache, fetch it from the database
        stock_data = StockData.objects.all()
        serializer = StockDataSerializer(stock_data, many=True)
        stock_data_list = serializer.data

        # Store the entire list in the cache for future requests
        cache.set(cache_key, stock_data_list, timeout=5)  # Cache for 15 minutes
        print("\n\n -------------- Not In cache -----------\n \n")
        return Response(stock_data_list, status=status.HTTP_200_OK)


class StockDataDetailView(generics.RetrieveAPIView):
    queryset = StockData.objects.all()
    serializer_class = StockDataSerializer
    lookup_field = 'ticker'

    def get(self, request, *args, **kwargs):
        ticker = self.kwargs.get('ticker')
        cache_key = f'stock_data:{ticker}'
        
        # Check if the individual data point is in the cache
        stock_data = cache.get(cache_key)

        if stock_data is not None:
            # If data is found in the cache, return it
            print("\n\n -------------- In cache -----------\n \n")
            return Response(stock_data, status=status.HTTP_200_OK)

        try:
            # If data is not in the cache, fetch it from the database
            stock_data_instance = StockData.objects.get(ticker=ticker)
            serializer = StockDataSerializer(stock_data_instance)
            stock_data = serializer.data

            # Store the individual data point in the cache for future requests
            cache.set(cache_key, stock_data, timeout=5)  # Cache for 5 seconds
            print("\n\n -------------- Not In cache -----------\n \n")
            return Response(stock_data, status=status.HTTP_200_OK)
        except StockData.DoesNotExist:
            return Response({"detail": "Stock data not found"}, status=status.HTTP_404_NOT_FOUND)
