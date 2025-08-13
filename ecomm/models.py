from typing import Any
from django.db import models
from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    stock = models.IntegerField()
    
    # def __init__(self):
    #     return self.name


