from django.urls import path
from .views import ProductView


urlpatterns = [
    path('products/analytics', ProductView.as_view())
]

