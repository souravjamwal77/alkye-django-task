from rest_framework import serializers
from .models import Product



"""{
  "total_products": 1200,
  "average_price": 45.67,
  "total_stock_value": 150000.00
}


"""

class ProductSerializers(serializers.Serializer):
    total_products = serializers.IntegerField()
    average_price = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_stock_value = serializers.DecimalField(max_digits=20, decimal_places=2)



