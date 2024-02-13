from django.db import models


# CUstomer

class Customer_Model(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_address = models.TextField()
    customer_mobile = models.BigIntegerField()
    customer_balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.customer_name

# user


class User_Model(models.Model):
    type_choice = (("admin", "admin"), ("member", "member"))
    user_status_choice = (("active", "active"), ("inactive", "inactive"))

    user_email = models.EmailField()
    user_password = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100, choices=type_choice)
    user_status = models.CharField(max_length=100, choices=user_status_choice)

    def __str__(self):
        return self.user_name

# supplier


class Supplier_Model(models.Model):
    supplier_status_choices = (("active", "active"), ("inactive", "inactive"))

    supplier_name = models.CharField(max_length=200)
    supplier_mobile = models.BigIntegerField()
    supplier_address = models.TextField()
    supplier_status = models.CharField(
        max_length=200, choices=supplier_status_choices, default="active")

    def __str__(self):
        return self.supplier_name

# category


class Category_Model(models.Model):
    category_status_choice = (("active", "active"), ("inactive", "inactive"))

    category_name = models.CharField(max_length=200)
    category_status = models.CharField(
        max_length=200, choices=category_status_choice, default="active")

    def __str__(self):
        return self.category_name

# brand


class Brand_Model(models.Model):
    brand_status_choice = (("active", "active"), ("inactive", "inactive"))

    category_id = models.ForeignKey(
        Category_Model, on_delete=models.CASCADE, default=True, null=False, blank=False)
    brand_name = models.CharField(max_length=200)
    brand_status = models.CharField(
        max_length=200, choices=brand_status_choice, default="active")

    def __str__(self):
        return self.brand_name


# product
class Product_Model(models.Model):
    product_status_choice = (("active", "active"), ("inactive", "inactive"))

    category_id = models.ForeignKey(Category_Model, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(Brand_Model, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_model = models.CharField(max_length=200)
    product_description = models.TextField()
    product_quantity = models.IntegerField()
    product_unit = models.CharField(max_length=200)
    product_base_price = models.FloatField()
    product_tax = models.DecimalField(max_digits=12, decimal_places=2)

    product_supplier = models.ForeignKey(
        Supplier_Model, on_delete=models.CASCADE)
    product_status = models.CharField(
        max_length=200, choices=product_status_choice, default="active")
    product_date = models.DateField()

    def __str__(self):
        return self.product_name

# Purchase


class Purchase_Model(models.Model):

    Supplier_id = models.ForeignKey(Supplier_Model, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product_Model, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.purchase_id


# order

class Order_Model(models.Model):

    product_id = models.ForeignKey(Product_Model, on_delete=models.CASCADE)
    total_shipped = models.IntegerField()
    customer_id = models.ForeignKey(Customer_Model, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.order_id
