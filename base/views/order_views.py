from django.shortcuts import render
from base.models import Category, Customer, Order, OrderDetail


# create new order
def order_create_view(request, pk):
    customer = Customer.objects.get(pk=pk)
    categoires = Category.objects.all()
    context = {
        "customer" : customer, 
        "categories" : categoires
    }
    return render(request, "base/orders/create.html", context)

