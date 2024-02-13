from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# login page


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'login.html')

# home (inventory)


@login_required
def home(request):
    search_query = request.GET.get('search')  # Move this line up

    if search_query:
        products = Product_Model.objects.filter(
            product_name__icontains=search_query)
    else:
        products = Product_Model.objects.all()
    # purchases
    purchases = Purchase_Model.objects.all()
    # customer
    orders = Order_Model.objects.all()
    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    search_query = request.GET.get('search')


# {{ product.product_quantity }}
# +
# {% for purchase in purchases %}
#   {% if purchase.product_id.product_name == product.product_name %}
#     {{ purchase.quantity }}
#   {% endif %}
# {% endfor %}
# -
# {% for order in orders %}
#   {% if order.product_id.product_name == product.product_name %}
#     {{ order.total_shipped }}
#   {% endif %}
# {% endfor %}

    # for product in products:
    #     total_quantity = product.product_quantity

    #     for purchase in purchases.filter(product_id__product_name=product.product_name):
    #         total_quantity += purchase.quantity

    #     for order in orders.filter(product_id__product_name=product.product_name):
    #         total_quantity -= order.total_shipped

    #     product_data = {'product': product, 'total_quantity': total_quantity}
    #     context['products_data'].append(product_data)
    values = []
    for product in products:
        starting_inventory = product.product_quantity
        purchaseq = 0
        inventory_shipped = 0

        for purchase in purchases:
            if purchase.product_id.product_name == product.product_name:
                purchaseq = purchase.quantity
                break

        for order in orders:
            if order.product_id.product_name == product.product_name:
                inventory_shipped = order.total_shipped
                break

        total_inventory = starting_inventory + purchaseq - inventory_shipped

        values.append({
            'product_name': product.product_name,
            'starting_inventory': starting_inventory,
            'purchase_quantity': purchaseq,
            'inventory_shipped': inventory_shipped,
            'total_inventory': total_inventory
        })


#            {% for order in orders %}
#   {% if order.product_id.product_name == product.product_name %}
#     {{ order.total_shipped }}
#   {% endif %}
# {% endfor %}
    # productt.append(product.product_name)
    # starting_inventory += product.product_quantity

    context = {
        "products": products,
        "purchases": purchases,
        "orders": orders,
        "values": values
    }

    return render(request, 'inventory.html', context)

# customer page


@login_required
def customer(request):
    search_query = request.GET.get('search')
    if search_query:
        customer_data = Customer_Model.objects.filter(
            customer_name__icontains=search_query)
    else:
        customer_data = Customer_Model.objects.all()

    paginator = Paginator(customer_data, 4)
    page_number = request.GET.get('page')
    final_customer_data = paginator.get_page(page_number)
    if request.method == "POST":

        Customer_name = request.POST.get('customer_name')
        Customer_address = request.POST.get('customer_address')
        Customer_mobile = request.POST.get('customer_mobile')
        Customer_balance = request.POST.get('customer_balance')
        customer = Customer_Model(customer_name=Customer_name, customer_address=Customer_address,
                                  customer_mobile=Customer_mobile, customer_balance=Customer_balance)
        customer.save()
        messages.info(request, "customer added successfully")
        return redirect('customer')

    context = {
        "customers": final_customer_data
    }

    return render(request, 'customer.html', context)

# customer delete


@login_required
def customer_delete(request, id):
    data = Customer_Model.objects.get(id=id)
    name = data.customer_name
    data.delete()
    messages.info(request, f"{name} data deleted successfully")
    return redirect('customer')

# customer edit


@login_required
def customer_update(request):
    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        customer_mobile = request.POST.get('customer_mobile')
        customer_balance = request.POST.get('customer_balance')
        customer_address = request.POST.get('customer_address')
        customer_id = request.POST.get('id')
        customer = Customer_Model.objects.get(id=customer_id)
        customer.customer_name = customer_name
        customer.customer_address = customer_address
        customer.customer_mobile = customer_mobile
        customer.customer_balance = customer_balance
        customer.save()
        messages.info(request, "customer updated successfully")
        return redirect('customer')


# category list page

@login_required
def category(request):
    search_query = request.GET.get('search')
    if search_query:
        category_data = Category_Model.objects.filter(
            category_name__icontains=search_query
        )
    else:
        category_data = Category_Model.objects.all()

    paginator = Paginator(category_data, 4)
    page_number = request.GET.get('page')
    final_category_data = paginator.get_page(page_number)

    if request.method == "POST":
        category_name = request.POST.get('category_name')
        name = category_name
        category = Category_Model(category_name=category_name)
        category.save()
        messages.info(request, f"{name} category added successfully")
        return redirect('category')
    context = {
        "categories": final_category_data
    }
    return render(request, 'category.html', context)

# category deleting


@login_required
def category_delete(request, id):

    data = Category_Model.objects.get(id=id)
    name = data.category_name
    data.delete()
    messages.info(request, f"{name} category deleted successfully")
    return redirect('category')

# update category


@login_required
def update_category(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        category_id = request.POST.get('category_id')
        category = Category_Model.objects.get(id=category_id)
        category.category_name = category_name
        category.save()
        messages.info(
            request, f"{category_name} category updated successfully")
        return redirect('category')

# brand list page


@login_required
def brand(request):
    # getting the category
    categories = Category_Model.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        brand_data = Brand_Model.objects.filter(
            brand_name__icontains=search_query
        )
    else:
        brand_data = Brand_Model.objects.all()
    paginator = Paginator(brand_data, 4)
    page_number = request.GET.get('page')
    brand_data = paginator.get_page(page_number)

    if request.method == "POST":
        brand_name = request.POST.get('brand_name')
        category_name = request.POST.get('category_name')
        try:
            # Convert the category_id to a Category_Model instance
            category_instance = Category_Model.objects.get(pk=category_name)
        except Category_Model.DoesNotExist:
            # Handle the case where the specified Category_Model does not exist
            # You may want to add appropriate error handling here
            messages.error(request, 'Category not found')
            return redirect('brand')
        brand = Brand_Model(brand_name=brand_name,
                            category_id=category_instance)
        brand.save()
        messages.info(request, f"{brand_name} brand added successfully")
        return redirect('brand')
    context = {
        "categories": categories,
        "brands": brand_data
    }
    return render(request, 'brand.html', context)

# brand deleting


@login_required
def brand_delete(request, id):
    brand = Brand_Model.objects.get(id=id)
    brand.delete()
    messages.info(request, f"{brand.brand_name} brand deleted successfully")
    return redirect('brand')


# update brand
@login_required
def update_brand(request):
    if request.method == "POST":
        brand_name = request.POST.get('brand_name')
        category_name = request.POST.get('category_name')
        brand_id = request.POST.get('bid')
        try:
            # Convert the category_id to a Category_Model instance
            category_instance = Category_Model.objects.get(pk=category_name)
        except Category_Model.DoesNotExist:
            # Handle the case where the specified Category_Model does not exist
            # You may want to add appropriate error handling here
            messages.error(request, 'Category not found')
            return redirect('brand')
        brand = Brand_Model(
            id=brand_id,
            brand_name=brand_name,
            category_id=category_instance)
        brand.save()

        messages.info(

            request, f"{brand_name} brand updated successfully")
        return redirect('brand')

# supplier list


@login_required
def supplier(request):
    search_query = request.GET.get('search')
    if search_query:
        suppliers = Supplier_Model.objects.filter(
            supplier_name__icontains=search_query
        )
    else:
        suppliers = Supplier_Model.objects.all()
    paginator = Paginator(suppliers, 4)
    page_number = request.GET.get('page')
    suppliers = paginator.get_page(page_number)
    if request.method == "POST":
        supplier_name = request.POST.get('supplier_name')
        supplier_mobile = request.POST.get('supplier_mobile')
        supplier_address = request.POST.get('supplier_address')
        supplier = Supplier_Model(
            supplier_name=supplier_name, supplier_mobile=supplier_mobile, supplier_address=supplier_address)
        supplier.save()
        messages.info(request, f"{supplier_name} supplier added successfully")
        return redirect('supplier')
    context = {
        "suppliers": suppliers
    }
    return render(request, 'supplier.html', context)

# delete supplier


@login_required
def supplier_delete(request, id):
    supplier = Supplier_Model.objects.get(id=id)
    supplier.delete()
    messages.info(
        request, f"{supplier.supplier_name} supplier deleted successfully")
    return redirect('supplier')

# update supplier


@login_required
def update_supplier(request):
    if request.method == "POST":

        supplier_name = request.POST.get('supplier_name')
        supplier_id = request.POST.get('supplier_id')
        supplier_mobile = request.POST.get('supplier_mobile')
        supplier_address = request.POST.get('supplier_address')
        supplier = Supplier_Model.objects.get(id=supplier_id)
        supplier.supplier_name = supplier_name
        supplier.supplier_mobile = supplier_mobile
        supplier.supplier_address = supplier_address
        supplier.save()
        messages.info(
            request, f"{supplier_name} supplier updated successfully")
        return redirect('supplier')


# product list

@login_required
def product(request):
    # getting category
    catigories = Category_Model.objects.all()
    # getting brand
    brands = Brand_Model.objects.all()
    # getting supplier
    suppliers = Supplier_Model.objects.all()
    # getting products
    search_query = request.GET.get('search')
    if search_query:
        products = Product_Model.objects.filter(
            product_name__icontains=search_query

        )
    else:

        products = Product_Model.objects.all()
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    if request.method == "POST":
        product_category = request.POST.get("product_category")
        product_brand = request.POST.get("product_brand")
        product_name = request.POST.get("product_name")
        product_model = request.POST.get("product_model")
        product_description = request.POST.get("product_description")
        product_quantity = request.POST.get("product_quantity")
        product_unit = request.POST.get("product_unit")
        product_base_price = request.POST.get("product_base_price")
        product_tax = request.POST.get("product_tax")
        supplier_name = request.POST.get("supplier_name")
        product_date = request.POST.get("product_date")
        try:
            # Convert the category_id to a Category_Model instance
            category_instance = Category_Model.objects.get(pk=product_category)
            brand_instance = Brand_Model.objects.get(pk=product_brand)
            supplier_instance = Supplier_Model.objects.get(pk=supplier_name)
        except Category_Model.DoesNotExist:
            messages.error(request, 'Try again')

        product = Product_Model(
            category_id=category_instance,
            brand_id=brand_instance,
            product_name=product_name,
            product_model=product_model,
            product_description=product_description,
            product_quantity=product_quantity,
            product_unit=product_unit,
            product_base_price=product_base_price,
            product_tax=product_tax,
            product_supplier=supplier_instance,
            product_date=product_date
        )
        product.save()
        messages.info(request, f"{product_name} product added successfully")
        return redirect('product')

    context = {
        "categories": catigories,
        "brands": brands,
        "suppliers": suppliers,
        "products": products
    }
    return render(request, 'product.html', context)

# deleting the product


@login_required
def product_deleting(request, id):
    product = Product_Model.objects.get(id=id)
    product.delete()
    messages.info(
        request, f"{product.product_name} product deleted successfully")
    return redirect('product')

# updating product


@login_required
def product_update(request):
    if request.method == "POST":
        product_category = request.POST.get("product_category")
        product_brand = request.POST.get("product_brand")
        product_name = request.POST.get("product_name")
        product_model = request.POST.get("product_model")
        product_description = request.POST.get("product_description")
        product_quantity = request.POST.get("product_quantity")
        product_unit = request.POST.get("product_unit")
        product_base_price = request.POST.get("product_base_price")
        product_tax = request.POST.get("product_tax")
        supplier_name = request.POST.get("supplier_name")
        product_id = request.POST.get("product_id")

        try:
            # Convert the category_id to a Category_Model instance
            category_instance = Category_Model.objects.get(pk=product_category)
            brand_instance = Brand_Model.objects.get(pk=product_brand)
            supplier_instance = Supplier_Model.objects.get(pk=supplier_name)
        except Category_Model.DoesNotExist:
            messages.error(request, 'Try again')

        product = Product_Model(
            id=product_id,
            category_id=category_instance,
            brand_id=brand_instance,
            product_name=product_name,
            product_model=product_model,
            product_description=product_description,
            product_quantity=product_quantity,
            product_unit=product_unit,
            product_base_price=product_base_price,
            product_tax=product_tax,
            product_supplier=supplier_instance,

        )
        product.save()
        messages.info(request, f"{product_name} product updated successfully")

        return redirect('product')
# purchase


@login_required
def purchase(request):
    # getting the products
    search_query = request.GET.get('search')
    if search_query:
        purchases = Purchase_Model.objects.filter(
            product_id__product_name=search_query
        )
    else:
        purchases = Purchase_Model.objects.all()

    paginator = Paginator(purchases, 4)
    page_number = request.GET.get('page')
    final_purchases = paginator.get_page(page_number)

    # getting supplier name
    suppliers = Supplier_Model.objects.all()
    # getting purchase data
    # purchases = Purchase_Model.objects.all()
    products = Product_Model.objects.all()
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        supplier_name = request.POST.get("supplier_name")
        quantity = request.POST.get("product_quantity")
        pruchase = Purchase_Model(
            product_id=Product_Model.objects.get(pk=product_name),
            Supplier_id=Supplier_Model.objects.get(pk=supplier_name),
            quantity=quantity
        )
        pruchase.save()
        messages.info(
            request, f"{product_name} product purchased successfully")
        return redirect('purchase')
    context = {
        "products": products,
        "suppliers": suppliers,
        "purchases": final_purchases
    }
    return render(request, 'purchase.html', context)

# purchase delete


@login_required
def purchase_delete(request, id):
    purchase = Purchase_Model.objects.get(id=id)
    purchase.delete()
    messages.info(
        request, f"{purchase.product_id.product_name} product deleted successfully")
    return redirect('purchase')

# update purchase


@login_required
def update_purchase(request):
    if request.method == "POST":
        purchase_id = request.POST.get("purchase_id")
        product_name = request.POST.get("product_name")
        supplier_name = request.POST.get("supplier_name")
        quantity = request.POST.get("product_quantity")
        pruchase = Purchase_Model(
            id=purchase_id,
            product_id=Product_Model.objects.get(pk=product_name),
            Supplier_id=Supplier_Model.objects.get(pk=supplier_name),
            quantity=quantity
        )
        pruchase.save()
        messages.info(
            request, f"{product_name} product purchase updated successfully")
        return redirect('purchase')


# manage page

@login_required
def manage_page(request):
    # getting the products
    products = Product_Model.objects.all()
    # getting customer
    customers = Customer_Model.objects.all()
    # getting orders data
    search_query = request.GET.get('search')
    if search_query:
        orders = Order_Model.objects.filter(
            product_id__product_name=search_query

        )
    else:
        orders = Order_Model.objects.all()
    paginator = Paginator(orders, 4)
    page_number = request.GET.get('page')
    orders_final = paginator.get_page(page_number)

    # posting the data to the database
    if request.method == "POST":
        product = Product_Model.objects.get(id=request.POST.get("product_id"))
        product_name = request.POST.get("product_id")
        customer_name = request.POST.get("customer_id")
        total_item = request.POST.get("total_item")
        orders = Order_Model(
            product_id=Product_Model.objects.get(pk=product_name),
            customer_id=Customer_Model.objects.get(pk=customer_name),
            total_shipped=total_item
        )
        orders.save()
        messages.info(
            request, f"{product.product_name} product ordered successfully")
        return redirect('manage_page')
    context = {
        "products": products,
        "customers": customers,
        "orders": orders_final
    }
    return render(request, 'manage.html', context)

# order delete


@login_required
def order_delete(request, id):
    order = Order_Model.objects.get(id=id)
    order.delete()
    messages.info(
        request, f"{order.product_id.product_name} product deleted successfully")
    return redirect('manage_page')

# updating the order page


@login_required
def upadate_manage_page(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        product_id = request.POST.get("product_id")
        customer_id = request.POST.get("customer_id")
        total_item = request.POST.get("total_item")

        try:
            product = Product_Model.objects.get(pk=product_id)
            customer = Customer_Model.objects.get(pk=customer_id)

            order = Order_Model(
                id=order_id,
                product_id=product,
                customer_id=customer,
                total_shipped=total_item
            )

            order.save()

            messages.info(
                request, f'{product.product_name} product order updated successfully'
            )

            return redirect('manage_page')

        except Product_Model.DoesNotExist:
            messages.error(request, "Product does not exist")
        except Customer_Model.DoesNotExist:
            messages.error(request, "Customer does not exist")

    return redirect('manage_page')
