from django.shortcuts import render
from rest_framework import viewsets, filters, status
from .models import Category, Brand, Firm, Product, Purchases
from .serializers import CategorySerializer, CategoryProductSerializer, BrandSerializer, FirmSerializer, ProductSerializer, PurchasesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response


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

    def create (self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #Add Product Stock###
        purchase = request.data
        product = Product.objects.get(id=purchase['product_id'])
        product.stock += purchase['quantity']
        product.save()
        ####
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        #Add Product Stock###
        purchase = request.data
        product = Product.objects.get(id=instance.product_id)
        updated_quantity = purchase['quantity'] - instance.quantity
        product.stock += updated_quantity
        product.save()
        ############################
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()    