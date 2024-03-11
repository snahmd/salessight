from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Category, Brand, Firm, Product, Purchases
from .serializers import CategorySerializer, CategoryProductSerializer, BrandSerializer, FirmSerializer, ProductSerializer, PurchasesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions



# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ['name']
    filterset_fields = ['name']
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.query_params.get('name'):
            return CategoryProductSerializer
        return super().get_serializer_class()

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    permission_classes = [DjangoModelPermissions]


class FirmViewSet(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    permission_classes = [DjangoModelPermissions]    


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ['category', 'brand']
    search_fields = ['name']
    permission_classes = [DjangoModelPermissions]    


class PurchasesViewSet(viewsets.ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = [ 'product', 'firm']
    search_fields = ['firm']
    permission_classes = [DjangoModelPermissions]
