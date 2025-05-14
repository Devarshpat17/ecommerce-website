from rest_framework import serializers
from store.models import Product, Category  # Adjust the import based on your actual models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # You can specify the fields you want to include

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # You can specify the fields you want to include