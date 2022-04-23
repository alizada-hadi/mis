from decimal import Decimal
from django.shortcuts import redirect, render
from base.models import ExpenseCategory, Expense
from django.contrib import  messages
from base.forms.expense_forms import ExpenseForm
from jalali_date import datetime2jalali, date2jalali
from datetime import datetime

# list expenses
def expense_list_view(request):
    expenses = Expense.objects.all()
    context = {
        "expenses" : expenses
    }

    return render(request, "base/expenses/list_create.html", context)


# create new expenses
def create_expense_view(request):
    categorires = ExpenseCategory.objects.all()
    if request.method == "POST":
        category = ExpenseCategory.objects.get(category_name=request.POST.get("category"))
        # optional fields
        product_name = request.POST.get("product_name")
        product_qty  = request.POST.get("product_qty")
        if not product_qty:
            product_qty = Decimal(1)
        rant = request.POST.get("rant")
        from_place = request.POST.get("from")
        to_place = request.POST.get("to")
        alternative = request.POST.get("alternative")
        if not alternative:
            alternative = Decimal(1)
        paid_amount = request.POST.get("paid_amount")
        amount = request.POST.get("amount")
        unit = request.POST.get("price_unit")
        if unit == "afg":
            unit =  "افغانی"
        elif unit == "usd":
            unit = "دالر"
        elif unit == "kaldar":
            unit = "کلدار"
        elif unit == "toman":
            unit = "تومان"
        date = request.POST.get("exp_date")
        desc = request.POST.get("exp_desc")
        Expense.objects.create(
        category=category, 
        exp_amount = Decimal(amount), 
        price_unit=unit, 
        exp_date = date, 
        good_name=product_name, 
        exp_quantity=Decimal(product_qty), 
        rant_month=rant, 
        from_place=from_place, 
        to_place=to_place, 
        paid_amount=Decimal(paid_amount),
        alternative=Decimal(alternative), 
        exp_description=desc
    )
        messages.success(request, "مصارف شما موفقانه ثبت گردید. ")
        return redirect("create-expense")

    context = {
        "categorires" : categorires
    }
    return render(request, 'base/expenses/create.html', context)



# delete expense item view

def delete_expense_view(request):
    if request.method == "POST":
        expense = Expense.objects.get(pk=request.POST.get("exp_id"))
        try:
            expense.delete()
            messages.success(request, "مورد فوق موفقانه از لیست مصارف شما حذف گردید. ")
        except:
            messages.error(request, "اشتباهی رخ داد، لطفا چک کرده و دوباره تلاش کنید. ")
        return redirect("expense-list")


# expense detail and generate pdf file

def expense_detail_view(request, pk):
    expense = Expense.objects.get(pk=pk)
    context = {
        "expense": expense
    }
    return render(request, "base/expenses/detail.html", context)



# annual expenses
def annual_expense_view(request):
    # expenses = Expense.objects.filter(exp_date="")
    # convert year from miladi to hijri
    # finding the current date and time in miladi
    now = datetime.now()
    # now convert it to year in hijri 
    current_year_in_hijri = date2jalali(now).strftime("%Y")
    
    # next filter and get the expenses in this year
    expenses = Expense.objects.filter(exp_date__year=current_year_in_hijri)

    # get the total expenses in AFG
    total = 0
    paid_amount = 0
    remain_amount = 0
    for exp in expenses:
        total += exp.total
        paid_amount += exp.paid_amount
        remain_amount += exp.remain_amount

    context = {
        "expenses" : expenses, 
        "current_year_in_hijri" : current_year_in_hijri, 
        "total" : total, 
        "paid_amount" : paid_amount, 
        "remain_amount" : remain_amount
    }
    return render(request, "base/expenses/annual_exp.html", context)




