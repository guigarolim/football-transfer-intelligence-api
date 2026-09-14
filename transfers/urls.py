from django.urls import path
from .views import TransferListView, TransferDetailView

urlpatterns = [
    path('transfers/', TransferListView.as_view(), name='transfer-list'),
    path('transfers/<int:pk>/', TransferDetailView.as_view(), name='transfer-detail'),
]