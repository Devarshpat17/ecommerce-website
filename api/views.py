from rest_framework import viewsets
from store.models import Product, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

def save_file(file, path):
    if default_storage.exists(path):
        # Generate a unique name if the file or directory already exists
        path = default_storage.get_available_name(path)
    return default_storage.save(path, ContentFile(file.read()))
