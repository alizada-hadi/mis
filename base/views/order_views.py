from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.contrib import messages

from base.models import Category, Customer, EmployeeFee, Order, OrderDetail, Employee, Recieve, Income
from decimal import Decimal
from datetime import datetime
from jalali_date import date2jalali
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_groups

# recieve money
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def recieve_view(request):
    if request.method == "POST":
        order = Order.objects.get(id=request.POST.get("order"))
        amount = request.POST.get("amount")
        amount_letter = request.POST.get("amount_letter")
        recieved_date = request.POST.get("recieve_date")

        obj = Recieve.objects.create(
            order=order, 
            amount=amount, 
            amount_letter=amount_letter, 
            recived_at=recieved_date
        )
        title = f"دریافت پول از {order.customer.first_name} - {order.customer.last_name}"
        price_unit = "افغانی"
        alternative = Decimal(1)
        if obj:
            Income.objects.create(
                income_title = title, 
                amount = Decimal(amount),
                price_unit=price_unit, 
                alternative=alternative, 
                recieved_at=recieved_date
            )
            order.total_amount = order.total_amount - (Decimal(amount) + Decimal(order.paid_amount))
            order.save()
            messages.success(request, f"شما به مقدار {amount} افغانی دریافت کردید. ")
            return redirect("create-order" ,order.customer.id)
        else:
            messages.error(request, "مشکلی رخ داد، لطفا دوباره تلاش کنید. ")
            return redirect("create-order" ,order.customer.id)


# recieve list
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def recieve_list_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    orders = customer.order_set.all()
    recieves = []

    for order in orders:
        for r in order.recieve_set.all():
            recieves.append(r)

    context = {
        "customer" : customer, 
        "orders" : orders, 
        "recieves" : recieves
    }
    return render(request, "base/orders/recieve_list.html", context)

# delete recieve amount
def delete_recieve(request, pk, order_id):
    order = get_object_or_404(Order, pk=order_id)
    recieve = get_object_or_404(Recieve, pk=pk)
    if request.method == "POST":
        recieve.delete()
        return redirect("recieve-list", order.id)
    return render(request, "base/orders/delete_recieve.html")

# create new order
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def order_create_view(request, pk):
    customer = Customer.objects.get(pk=pk)
    orders = customer.order_set.all()
    now = datetime.now()
    date_in_hijri = date2jalali(now).strftime("%Y-%m-%d")
    # total 
    total = 0
    get_amount_per_order = 0
    remain_total_amount = 0
    recieved_amount = 0
    last_recieved_at = ""
    for i in orders:
        for j in i.orderdetail_set.all():
            total += j.total
    for k in orders:
        for m in k.recieve_set.all():
            get_amount_per_order += (Decimal(m.amount))
            recieved_amount += (m.amount)
        get_amount_per_order += k.paid_amount
        recieved_amount += k.paid_amount
    remain_total_amount = total - get_amount_per_order

    for d in orders:
        last_recieved_at = d.recieve_set.last()

    if request.method == "POST":
        order = Order.objects.create(
            customer=customer,
            paid_amount = 0,
            total_amount = 0, 
            date_ordered = date_in_hijri
        )
        if order:
            messages.success(request, "فرمایش جدید موفقانه ثبت گردید.")
            return redirect("order-detail", order.id)
        else:
            messages.error(request, "اشتباه رخ داد، لطفا دوباره سعی کنید.")
            return redirect("create-order", customer.pk)
            
    context = {
        "customer" : customer, 
        "orders" : orders, 
        "total" : total, 
        'remain_total_amount' : remain_total_amount, 
        "recieved_amount" : recieved_amount, 
        "last_recieved_at" : last_recieved_at
    }
    return render(request, "base/orders/create.html", context)


# update order
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def order_update_view(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == "POST":
        customer = Customer.objects.get(pk=request.POST.get("customer"))
        amount = request.POST.get("pre_paid")
        title = f"دریافت بیانه از {order.customer.first_name} {order.customer.last_name}"
        now = datetime.now()
        date_in_hijri = date2jalali(now).strftime("%Y-%m-%d")
        try:
            Income.objects.create(
                income_title = title, 
                amount=Decimal(amount), 
                recieved_at=date_in_hijri, 
                alternative=Decimal(1), 
                price_unit="افغانی"
            )
            order.customer=customer
            order.paid_amount=amount
            order.save()
            messages.success(request, "مقدار پیش پرداخت موفقانه ثبت سیستم گردید.")
            return redirect("order-detail", order.id)
        except:
            messages.error(request, "مشکل رخ داد، لطفا دوباره تلاش کنید.")
            return redirect("order-detail", order.id)



# delete order
def order_delete_view(request):
    if request.method == "POST":
        order = Order.objects.get(pk=request.POST.get("order_id"))
        try:
            order.delete()
            messages.success(request, "فرمایش شما موفقانه از سیستم حذف گردید. ")
            return redirect("create-order", order.customer.id)
        except:
            messages.error(request, "مشکلی رخ داد، لطفا دوباره تلاش کنید. ")
            return redirect("create-order", order.customer.id)


# order detail
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def order_detail_view(request, pk):
    categories = Category.objects.all()
    order = Order.objects.get(pk=pk)
    employees = Employee.objects.filter()
    items = order.orderdetail_set.all()
    # report start
    items_count = order.orderdetail_set.all().count()
    total_amount = 0
    remain_amount = 0
    for amount in order.orderdetail_set.all():
        total_amount += amount.total
        remain_amount = total_amount - order.paid_amount
    # report end
    # employee

    if request.method == "POST":
        category = Category.objects.get(name=request.POST.get("category"))
        quantity = request.POST.get("qty")
        price = request.POST.get("price")
        price_unit = request.POST.get("price_unit")
        alternative = request.POST.get("alternative")
        if alternative == "":
            alternative = Decimal(1)
        
        if  price_unit == 'afg':
            price_unit = "افغانی"
        if price_unit == "usd":
            price_unit = "دالر"
        if price_unit == "toman":
            price_unit = "تومان"
        if price_unit == "kaldar":
            price_unit = "کلدار"
        work_type = request.POST.get("work_type")
        vacum = request.POST.get("with_vacum")
        if vacum == "color":
            vacum = "رنگ"
        elif vacum == "vacum":
            vacum = "واکیوم"
        height =  request.POST.get("height")
        width = request.POST.get("width")
        depth = request.POST.get("depth")
        direction = request.POST.get("direction")
        with_color = request.POST.get("with_color")
        if with_color == "yes":
            with_color = "بلی"
        elif with_color == "no":
            with_color = "نخیر"
        if height == "" and width == "" and depth == "":
            height, width, depth = Decimal(0), Decimal(0), Decimal(0)
        if direction == "right":
            direction = "راست"
        elif direction == "left":
            direction = 'چپ'

        try:
            OrderDetail.objects.create(
            order=order, 
            category=category, 
            height=height, 
            width=width, 
            depth=depth, 
            direction=direction, 
            vacum=vacum,
            quantity=Decimal(quantity), 
            price=Decimal(price), 
            alternative=Decimal(alternative),
            price_unit=price_unit,
            type=work_type, 
            )
            order.total_amount += Decimal(quantity) * Decimal(price)
            order.save()
            messages.success(request, f"جزییات فرمایش نمبر {order.id} موفقانه ثبت سیستم گردید.")
            return redirect("order-detail", order.id)
        except:
            messages.error(request, "مشکلی رخ داد، لطفا دوباره سعی کنید.")
            return redirect("order-detail", order.id)
            
    context = {
        "order" : order, 
        "categories" : categories, 
        "employees" : employees, 
        "items_count" : items_count, 
        "total_amount" : total_amount, 
        "remain_amount" : remain_amount, 
        "items" : items
    }
    return render(request, "base/orders/create_detail.html", context)



def order_detail_delete(request):
    if request.method == "POST":
        order_detail = OrderDetail.objects.get(pk=request.POST.get("order_detail_id"))
        try:
            order_detail.delete()
            messages.success(request, "جزییات فرمایش فوق موفقانه از سیستم حذف گردید. ")
        except:
            messages.error(request, "مشکل رخ داد، لطفا چک کرده و دوباره تلاش کنید. ")
        
        return redirect("order-detail", order_detail.order.id)


@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def employee_generate_pdf(request, pk):
    order = Order.objects.get(pk=pk)
    items = order.orderdetail_set.all()

    context = {
        "items" : items, 
        "order" :order
    }
    html_string = render_to_string(
        "base/orders/employee_pdf.html", context
    )
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'inline; filename=emp_order_{order.id}.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())
    
    return response


@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def customer_generate_pdf(request, pk):
    order = Order.objects.get(pk=pk)
    items = order.orderdetail_set.all()

    total_amount = 0
    remain_amount = 0
    for amount in order.orderdetail_set.all():
        total_amount += amount.total
        remain_amount = total_amount - order.paid_amount

    context = {
        "order":order, 
        "items" : items, 
        "total_amount" : total_amount, 
        'remain_amount' : remain_amount
    }

    html_string = render_to_string(
        "base/orders/customer_pdf.html", 
        context
    )
    html = HTML(string=html_string)
    result = html.write_pdf()

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'inline; filename=customer_order_{order.id}.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())
    
    return response






# specify which employees work on a specific order_detail
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def employee_work_view(request, pk):
    order_detail = OrderDetail.objects.get(pk=pk)
    order = order_detail.order
    employees = Employee.objects.all()
    objects =  EmployeeFee.objects.filter(order_detail=order_detail)
    if request.method == "POST":
        emp = Employee.objects.get(id=request.POST.get("emp"))
        fee = request.POST.get("fee")
        obj = EmployeeFee.objects.create(
            order_detail=order_detail, 
            employee=emp, 
            fee=fee
        )
        if obj:
            messages.success(request, "کارمند جدید برای فرمایش فوق تعیین شد. ")
            return redirect("add-employee", order_detail.id)
        else:
            messages.error(request, "مشکلی رخ داد لطفا دوباره تلاش کنید. ")
            return redirect("add-employee", order_detail.id)
    context = {
        "order_detail": order_detail, 
        "order" : order, 
        "employees" : employees, 
        "objects" : objects
    }
    return render(request, "base/orders/employee_work.html", context)


def delete_employee_work_view(request):
    if request.method == "POST":
        work = EmployeeFee.objects.get(pk=request.POST.get("work"))
        try:
            work.delete()
            messages.success(request, "مورد فوق موفقانه حذف گردید. ")
        except:
            messages.error(request, "مشکلی رخ داد، لطفا چک کرده و دوباره تلاش کنید. ")
        return redirect("add-employee", work.order_detail.id)





