from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields= ("id","name", "description", "price", "quantity", "instruction","Ingredient","origin","IsActive","category", "priceSale", "IsFlashsale","brand")
        skip_unchange = True
        report_skipped = False
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource


class IngredientsResource(resources.ModelResource):
    class Meta:
        model = Ingredients
        fields= ("id","name", "levelOfSave", "Description","slug")
        skip_unchange = True
        report_skipped = False

class IngredientsAdmin(ImportExportModelAdmin):
    resource_class = IngredientsResource

#=======================
class ProductTypeResource(resources.ModelResource):
    class Meta:
        model = ProductType
        fields= ("id","name")
        skip_unchange = True
        report_skipped = False

class ProductTypeAdmin(ImportExportModelAdmin):
    resource_class = ProductTypeResource
#=======================
class ProductCategoryResource(resources.ModelResource):
    class Meta:
        model = ProductCategory
        fields= ("id","name","producttype")
        skip_unchange = True
        report_skipped = False

class ProductCategoryAdmin(ImportExportModelAdmin):
    resource_class = ProductCategoryResource

# Register your models here.
admin.site.register(User)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductCategory,ProductCategoryAdmin)
admin.site.register(ProductImage)
admin.site.register(Rating)
admin.site.register(LoveList)
admin.site.register(IngredientsTag)
admin.site.register(Ingredients,IngredientsAdmin)
admin.site.register(Delivery)
admin.site.register(Order)
admin.site.register(DetailOrder)
admin.site.register(Cart)
admin.site.register(Provinces)
admin.site.register(Districts)
admin.site.register(Wards)
admin.site.register(ProductType,ProductTypeAdmin)
admin.site.register(Banner)