from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BrandViewSet, FirmViewSet, ProductViewSet, PurchasesViewSet

router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('brands', BrandViewSet)
router.register('firms', FirmViewSet)
router.register('products', ProductViewSet)
router.register('purchases', PurchasesViewSet)

urlpatterns = [
    
] + router.urls