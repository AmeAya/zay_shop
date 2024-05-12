from rest_framework.serializers import ModelSerializer
from .models import *


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'brand', 'thumb', 'images']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['brand'] = BrandSerializer(instance.brand, many=False).data
        representation['images'] = ProductImageSerializer(instance.images, many=True).data
        return representation
