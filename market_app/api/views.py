from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ManufacturerSerializer, ProductSerializer, ManufacturerUserSerializer
from market_app.models import ManufacturerUser, Manufacturer, Product
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


class ManufacturerList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ManufacturerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ManufacturerUserList(generics.ListCreateAPIView):
    queryset = ManufacturerUser.objects.all()
    serializer_class = ManufacturerUserSerializer

class ManufacturerUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ManufacturerUser.objects.all()
    serializer_class = ManufacturerUserSerializer

class ProductDetail(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ManufacturerProductListCreate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        manufacturer_id = self.kwargs['manufacturer_id']
        return Product.objects.filter(manufacturer_id = manufacturer_id)
    
    def perform_create(self, serializer):
        manufacturer_id = self.kwargs['manufacturer_id']
        serializer.save(manufacturer_id = manufacturer_id)