from django.contrib import admin
# Thêm ProductDetail vào dòng import này
from .models import Product, Category, Promotion, FlashSale, ProductDetail 
from .models import Supplier

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Promotion)
admin.site.register(FlashSale)
admin.site.register(ProductDetail)
