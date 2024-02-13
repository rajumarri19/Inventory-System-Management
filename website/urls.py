from django.urls import path
from .import views
urlpatterns = [
    path('', views.login_page, name='login'),
    path('home', views.home, name="home"),
    path('customer', views.customer, name="customer"),
    path('category', views.category, name="category"),
    path('brand', views.brand, name="brand"),
    path('supplier', views.supplier, name="supplier"),
    path('product', views.product, name="product"),
    path('purchase', views.purchase, name="purchase"),
    path('manage_page', views.manage_page, name="manage_page"),
    # deleting functions
    path('customer_delete/<int:id>', views.customer_delete, name="customer_delete"),
    path('category_delete/<int:id>', views.category_delete, name="category_delete"),
    path('brand_delete/<int:id>', views.brand_delete, name="brand_delete"),
    path('supplier_delete/<int:id>', views.supplier_delete, name="supplier_delete"),
    path('product_deleting/<int:id>',
         views.product_deleting, name="product_deleting"),
    path('purchase_delete/<int:id>', views.purchase_delete, name="purchase_delete"),
    path('order_delete/<int:id>', views.order_delete, name="order_delete"),
    # update function
    path('upadate_manage_page/', views.upadate_manage_page,
         name="upadate_manage_page"),
    path('update_category/', views.update_category, name="update_category"),
    path('customer_update/', views.customer_update, name="customer_update"),
    path('update_supplier/', views.update_supplier, name="update_supplier"),
    path('update_brand/', views.update_brand, name="update_brand"),
    path('update_purchase/', views.update_purchase, name="update_purchase"),
    path('upadate_manage_page/', views.upadate_manage_page,
         name="upadate_manage_page"),
    path('product_update/', views.product_update, name="product_update"),
]
