from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializers
from django.core.cache import cache

from django.db.models import Count, Sum, Avg, F

# Create your views here.



class ProductView(APIView):
    def get(self, request):
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        
        # Check cache for the query first
        cache_key = f"product-analytics{hash(frozenset(request.GET.items()))}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        query = Product.objects.all()
        
        if category:
            query = query.filter(category=category)
        if min_price:
            query = query.filter(price__gte=min_price)
        if max_price:
            query = query.filter(price__lte=max_price)
        
        print(len(query))
        
        data = query.aggregate(
            total_products=Count('id'),
            average_price=Avg('price'),
            total_stock_value=Sum(F('stock') + F('price'))
        )
        
        serializer = ProductSerializers(data)
        
        # set cache for 5 mins
        cache.set(cache_key, serializer.data, 60*5)
        
        return Response(serializer.data)
