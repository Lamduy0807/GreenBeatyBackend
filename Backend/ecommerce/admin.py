from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields= ("id","name", "description", "price", "quantity", "instruction","Ingredient","origin","category", "imagepresent")
        skip_unchange = True
        report_skipped = False
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

# Register your models here.
admin.site.register(User)
admin.site.register(Product,ProductAdmin)
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
admin.site.register(Banner)