from rest_framework import generics
from .models import Transfer
from .serializers import TransferSerializer

class TransferListView(generics.ListAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

class TransferDetailView(generics.RetrieveAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer