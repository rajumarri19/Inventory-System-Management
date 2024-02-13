from django.contrib import admin
from .import models

# customer
admin.site.register(models.Customer_Model)
# user
admin.site.register(models.User_Model)
# supplier
admin.site.register(models.Supplier_Model)
# category
admin.site.register(models.Category_Model)
# Brand
admin.site.register(models.Brand_Model)
# product
admin.site.register(models.Product_Model)
# purchase
admin.site.register(models.Purchase_Model)
# order
admin.site.register(models.Order_Model)
