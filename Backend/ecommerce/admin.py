from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)
admin.site.register(Rating)
admin.site.register(LoveList)
admin.site.register(IngredientsTag)
admin.site.register(Ingredients)
admin.site.register(Delivery)
admin.site.register(Order)
admin.site.register(DetailOrder)
admin.site.register(Cart)
admin.site.register(Provinces)
admin.site.register(Districts)
admin.site.register(Wards)
admin.site.register(ProductType)
