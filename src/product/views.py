from rest_framework import generics
from rest_framework.permissions import AllowAny

from product.models import Product
from product.serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    """List products"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
