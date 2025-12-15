from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, ProductSerializer,SellerSerializer, SellerCreateSerializer, ProductDetailSerializer, ProductCreateSerializer
from market_app.models import Market, Seller, Product
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# mxixins views 
class MarketView(generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class MarketDetailView(generics.RetrieveUpdateDestroyAPIView, generics.GenericAPIView,):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

class SellerOfMarketList(generics.ListCreateAPIView):
    serializer_class = SellerSerializer
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk = pk)
        return market.sellers.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk = pk)
        serializer.save(markets = [market])
        pass

class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(user)
        return Response(serializer.data)


@api_view(['GET','POST'])
def market_view(request):

    if request.method =="GET":  
        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many = True, context = {'request': request} )
        return Response(serializer.data)
    
    
    if request.method == "POST":
        serializer = MarketSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

@api_view(['GET','DELETE', 'PUT'])
def single_market_view(request, pk):
    if request.method =="GET":  
        market = Market.objects.get(pk = pk)
        serializer = MarketSerializer(market, context={'request': request})
        return Response(serializer.data)
    
    if request.method =="PUT":  
        market = Market.objects.get(pk = pk)
        serializer = MarketSerializer(market, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    if request.method =="DELETE":  
        market = Market.objects.get(pk = pk)
        serializer = MarketSerializer(market)
        market.delete()
        return Response(serializer.data)

@api_view(['GET','POST'])
def seller_view(request):
    if request.method =="GET":
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many = True, context={'request': request} )
        return Response(serializer.data) 
    
    if request.method == "POST":
        serializer = SellerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET','DELETE', 'PUT'])
def single_seller_view(request, pk):
    if request.method == "GET":
        seller = Seller.objects.get(pk = pk)
        serializer = SellerSerializer(seller, context={'request': request})
        return Response(serializer.data)
    
    if request.method =="POST":
        pass
    

@api_view(['GET','POST'])
def product_view(request):
    if request.method =="GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many = True,context={'request': request} )
        return Response(serializer.data) 
    
    if request.method == "POST":
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
@api_view(['GET','DELETE', 'PUT'])
def single_product_view(request, pk):
    if request.method == "GET":
        product = Product.objects.get(pk = pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    
    if request.method =="POST":
        pass

