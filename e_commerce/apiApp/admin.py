from django.contrib import admin
from apiApp import models

admin.site.register(models.BrandModel)
admin.site.register(models.CategoryModel)
admin.site.register(models.ProductModel)
admin.site.register(models.UserCart)
admin.site.register(models.OrderDetailsModel)
admin.site.register(models.ReviewModel)


