from django.urls import path
from .views import TransactionCreateAPIView,TransactionUserListAPIView,TransactionInRangeAPIView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'transactions'

schema_view = get_schema_view(
   openapi.Info(
      title="Transaction API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('create/', TransactionCreateAPIView.as_view(), name='transaction-create'),
    path('<int:user_id>/', TransactionUserListAPIView.as_view(), name='get_user_transactions'),
    path('<int:user_id>/<str:start_timestamp>/<str:end_timestamp>/', TransactionInRangeAPIView.as_view(), name='user_transactions_in_range'),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
