from django.contrib import admin
from .models import Category, Product, OrderProduct, Order
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
