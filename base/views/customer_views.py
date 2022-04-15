from django.shortcuts import redirect, render
from base.models import Customer
from django.contrib import messages


# customer list
def customer_list_view(request):
    customers = Customer.objects.all()
    context = {
        "customers" : customers
    }

    return render(request, "base/customers/list.html", context)


# create new customer

def customer_create_view(request):
    if request.method == "POST":
        name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        social_number = request.POST.get("social_number")
        address = request.POST.get("address")

        try:
            Customer.objects.create(
                first_name=name, 
                last_name=last_name, 
                phone_number=phone_number, 
                social_number=social_number, 
                address=address
            )
            messages.success(request, "مشتری جدید موفقانه ثبت گردید.")
        except:
            messages.error(request, "مشکلی رخ داد، لطفا دوباره تلاش کنید.")
        return redirect("customer-list")


def update_customer(request):
    if request.method == "POST":
        customer = Customer.objects.get(pk=request.POST.get("customer"))
        name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        social_number = request.POST.get("social_number")
        address = request.POST.get("address")

        try:
            customer.first_name = name
            customer.last_name = last_name
            customer.phone_number = phone_number
            customer.social_number = social_number
            customer.address = address
            customer.save()
            messages.success(request, 'مشتری موفقانه ویرایش و دوباره ثبت سیستم گردید.')
        except:
            messages.error(request, "مشکلی رخ داد، لطفا دوباره تلاش کنید.")

        return redirect("customer-list")


# delete customer
def customer_delete_view(request):
    if request.method == "POST":
        customer = Customer.objects.get(pk = request.POST.get("customer"))
        try:
            customer.delete()
            messages.success(request, "یک مشتری موفقانه از سیستم حذف گردید.")
        except:
            messages.error(request, "مشکلی رخ داد، لطفا دوباره تلاش کنید.")

        return redirect("customer-list")

