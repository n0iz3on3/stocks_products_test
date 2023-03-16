from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['products']
    search_fields = ['products__title', 'products__description']
    ordering_fields = '__all__'


@api_view(['GET'])
def sample_view(request):
    return Response({'detail': 'This is checking!'})


@api_view(['GET'])
def some_view(request):
    return Response({'detail': 'All works!'})
