from django.views import View
from django.core.cache import cache
from .models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

# API to register user
class UserRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        balance = float(request.data.get('balance', 0.0))

        # Create a new user
        user = User.objects.create(username=username, balance=balance)

        # Serialize the user data
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UserDetailsAPIView(APIView):
    def get(self, request, username, *args, **kwargs):
        # Check if the user data is in the cache
        cache_key = f'user:{username}'
        user_data = cache.get(cache_key)

        if user_data is not None:
            # If data is found in the cache, return it
            print("\n\n -------------- In cache -----------\n \n")
            return Response(user_data, status=status.HTTP_200_OK)

        try:
            # If data is not in the cache, fetch it from the database
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            user_data = serializer.data
            # Store the user data in the cache for future requests
            cache.set(cache_key, user_data, timeout=5)  # Cache for 15 minutes
            print("\n\n -------------- Not in cache -----------\n \n")
            return Response(user_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


