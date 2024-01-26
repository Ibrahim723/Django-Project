from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse
from users.models import User
from stocks.models import StockData
from stocks.models import StockData
from datetime import datetime
from .models import Transaction
from .tasks import process_transaction
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TransactionSerializer
from dateutil.parser import isoparse

# class TransactionCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         user = request.data.get('username')
#         stock = request.data.get('ticker')
#         transaction_type = request.data.get('transaction_type')
#         transaction_volume = int(request.data.get('transaction_volume'))
#         transaction_price = float(request.data.get('transaction_price'))

#         # Parse the timestamp string into a datetime object
#         timestamp_str = request.data.get('timestamp')
#         timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")

#         # Get user and stock instance from the database
#         user_instance = User.objects.get(username=user)
#         stock_instance = StockData.objects.get(ticker=stock)

#         # Create a new transaction
#         transaction = Transaction.objects.create(
#             user=user_instance,
#             stock=stock_instance,
#             transaction_type=transaction_type,
#             transaction_volume=transaction_volume,
#             transaction_price=transaction_price,
#             timestamp=timestamp
#         )

#         # Serialize the transaction data
#         serializer = TransactionSerializer(transaction)
#         print("\n\n\n-------------",transaction.transaction_id,"-------\n\n")
#         # Trigger the Celery task asynchronously
#         process_transaction.delay(transaction.transaction_id)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class TransactionUserListAPIView(APIView):
    def get(self, request, user_id):
        try:
            transactions = Transaction.objects.filter(user_id=user_id)
            transaction_data = []
            for transaction in transactions:
                transaction_data.append({
                    'transaction_id': transaction.transaction_id,
                    'user_id': transaction.user_id,
                    'stock_id': transaction.stock_id,
                    'transaction_type': transaction.transaction_type,
                    'transaction_volume': transaction.transaction_volume,
                    'transaction_price': transaction.transaction_price,
                    'timestamp': transaction.timestamp.isoformat(),
                })

            response_data = {'transactions': transaction_data}
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TransactionCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        user = request.data.get('username')
        stock = request.data.get('ticker')
        transaction_type = request.data.get('transaction_type')
        transaction_volume = int(request.data.get('transaction_volume'))

        # Fetch the current stock instance from the database
        stock_instance = StockData.objects.get(ticker=stock)

        # Calculate the transaction price based on the current stock price
        transaction_price = transaction_volume * stock_instance.close_price

        # Parse the timestamp string into a datetime object
        timestamp_str = request.data.get('timestamp')
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Get user instance from the database
        user_instance = User.objects.get(username=user)

        # Check if the user has enough balance for the transaction
        if transaction_type == 'buy' and user_instance.balance < transaction_price:
            return Response({"detail": "Insufficient balance for the transaction."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's balance based on the transaction type
        if transaction_type == 'buy':
            user_instance.balance -= transaction_price
        elif transaction_type == 'sell':
            user_instance.balance += transaction_price

        # Save the updated user instance
        user_instance.save()

        # Create a new transaction
        transaction = Transaction.objects.create(
            user=user_instance,
            stock=stock_instance,
            transaction_type=transaction_type,
            transaction_volume=transaction_volume,
            transaction_price=transaction_price,
            timestamp=timestamp
        )

        # Serialize the transaction data
        serializer = TransactionSerializer(transaction)

        # Trigger the Celery task asynchronously
        process_transaction.delay(transaction.transaction_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TransactionInRangeAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        start_timestamp = self.kwargs['start_timestamp']
        end_timestamp = self.kwargs['end_timestamp']

        # Parse timestamps using dateutil.parser.isoparse
        start_datetime = isoparse(start_timestamp)
        end_datetime = isoparse(end_timestamp)

        # Filter transactions based on user and timestamp range
        return Transaction.objects.filter(
            user__id=user_id, timestamp__gte=start_datetime, timestamp__lte=end_datetime
        )


