from rest_framework import serializers
from store.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
           "id",
           "name",
           "description",
           "price",
           "image",
           "category",
           "stock",
]