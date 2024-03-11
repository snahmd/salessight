from rest_framework import serializers
from .models import Category, Product, Brand, Firm, Purchases, Sales    

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ("id", "name", "product_count")

    def get_product_count(self, obj):
        return Product.objects.filter(category_id=obj.id).count()  

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "category_id",
            "brand",
            "brand_id",
            "stock",
        )
        read_only_fields = ("stock",)   
        
class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ("id", "name", "product_count", "products")        

    def get_product_count(self, obj):
        return Product.objects.filter(category_id=obj.id).count()
    

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "image",
        )   

class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = (
            "id",
            "name",
            "phone",
            "image",
            "address",
        )      


class PurchasesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    firm = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    class Meta:
        model = Purchases
        fields = (
            "id",
            "user",
            "user_id",
            "firm",
            "firm_id",
            "product",
            "product_id",
            "brand",
            "brand_id",
            "quantity",
            "price",
            "price_total",
            "created_at",
            "updated_at",
        )   
        read_only_fields = ("price_total",) 

        def __str__(self):
            return f'{self.product.name} - {self.quantity}'