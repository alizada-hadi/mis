from django.shortcuts import redirect, render
from base.models import Customer, Exhibition
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_groups
from django.contrib import messages
from django.contrib.auth.models import User


@login_required(login_url="login")
def exhibition_list_create_view(request):
    exhibitions = Exhibition.objects.all()
    users = User.objects.exclude(username="admin")
    if request.method == "POST":
        user = User.objects.get(pk=request.POST.get("manager"))
        name = request.POST.get("name")
        address = request.POST.get("address")

        try:
            Exhibition.objects.create(
                manager = user, 
                name = name, 
                address = address
            )
            messages.success(request, "نمایشگاه جدید موفقانه ثبت گردید. ")
        except:
            messages.error(request, "مشکلی رخ داد لطفا بررسی کرده و دوباره تلاش کنید. ")
        return redirect("exhibition-list")
    context = {
        "exhibitions" : exhibitions, 
        "users" : users
    }

    return render(request, "base/exhibition/exhibition_list.html", context)







@login_required(login_url="login")
def my_customers(request):
    user = request.user
    customers = user.customer_set.all()

    context = {
        "customers" : customers
    }
    return render(request, "base/exhibition/list.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["manager"])
def create_new_customer(request):
    user = request.user
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        phone_number = request.POST.get('phone_number')
        social_number = request.POST.get('social_number')
        try:
            Customer.objects.create(
                add_by=user,
                first_name=first_name, 
                last_name=last_name, 
                address=address, 
                phone_number=phone_number, 
                social_number=social_number
            )
            messages.success(request, "مشتری جدید موفقانه ثبت گردید. ")
            return redirect("mine-customer-detail", Customer.objects.last().id)
        except:
            messages.error(request, "مشکلی رخ داد، لطفا دوباره تلاش کنید. ")
            return redirect("mine-customer-create")
    return render(request, "base/exhibition/create.html")



def my_customer_detail(request, pk):
    customer = Customer.objects.get(pk=pk)

    context = {
        "customer" : customer
    }
    return render(request, "base/exhibition/detail.html", context)


