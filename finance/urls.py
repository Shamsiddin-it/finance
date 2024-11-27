from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('income/', IncomeAPIView.as_view(), name = 'income_list'),
    path('income/<int:pk>/', IncomeRUDAPIView.as_view(), name = 'income_rud'),
    path('expence/', ExpenceAPIView.as_view(), name = 'expence_list'),
    path('expence/<int:pk>/', ExpenceRUDAPIView.as_view(), name = 'expence_rud'),
    path('wallet/', WalletAPIView.as_view(), name = 'wallet_list'),
    path('wallet/history/', WalletHistoryAPIView.as_view(), name = 'wallet_history'),
]
