from decimal import Decimal
from django.shortcuts import redirect, render
from base.models import ExpenseCategory, Expense
from django.contrib import  messages
from base.forms.expense_forms import ExpenseForm
from jalali_date import datetime2jalali, date2jalali
from datetime import datetime
import math
import datetime as my_time
from users.decorators import allowed_groups
from django.contrib.auth.decorators import login_required
from io import StringIO, BytesIO
import xlsxwriter
from django.http import HttpResponse



# list expenses
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def expense_list_view(request):
    expenses = Expense.objects.all()
    context = {
        "expenses" : expenses
    }

    return render(request, "base/expenses/list_create.html", context)


# create new expenses
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
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
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
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
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def expense_detail_view(request, pk):
    expense = Expense.objects.get(pk=pk)
    context = {
        "expense": expense
    }
    return render(request, "base/expenses/detail.html", context)



# annual expenses
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
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

    # get the expense ratio of last year expenses
    # first get the last year
    last_year_in_hijri = date2jalali(now).strftime("%Y")

    last_year_in_hijri = int(last_year_in_hijri) - 1
    last_year_expenses = Expense.objects.filter(exp_date__year=str(last_year_in_hijri))
    last_year_total_expense = 0
    for exp in last_year_expenses:
        last_year_total_expense += exp.total

    
    percentange = 0
    if last_year_total_expense == 0:
        percentange = 100
    else:
        percentange = (last_year_total_expense - total) / total * 100



    context = {
        "expenses" : expenses, 
        "current_year_in_hijri" : current_year_in_hijri, 
        "total" : total, 
        "paid_amount" : paid_amount, 
        "remain_amount" : remain_amount, 
        "percentange" : percentange
    }
    return render(request, "base/expenses/annual_exp.html", context)


# monthly expenses
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def monthly_expenses_view(request):
    # first get the full current date and time
    now = datetime.now()
    # second, find the current month in hijri
    current_month_in_hijri = date2jalali(now).strftime("%m")
    # third, filter the expenses based on the current month
    expenses = Expense.objects.filter(exp_date__month=current_month_in_hijri)
    # fourth, get the month's name
    month_name = ""
    if current_month_in_hijri == '01':
        month_name = "حمل"
    elif current_month_in_hijri == '02':
        month_name = "ثور"
    elif current_month_in_hijri == '03':
        month_name = "جوزا"
    elif current_month_in_hijri == '04':
        month_name = "سرطان"
    elif current_month_in_hijri == '05':
        month_name = "اسد"
    elif current_month_in_hijri == '06':
        month_name = "سنبله"
    elif current_month_in_hijri == '07':
        month_name = "میزان"
    elif current_month_in_hijri == '08':
        month_name = "عقرب"
    elif current_month_in_hijri == '09':
        month_name = "قوس"
    elif current_month_in_hijri == '10':
        month_name = "جدی"
    elif current_month_in_hijri == '11':
        month_name = "دلو"
    elif current_month_in_hijri == '12':
        month_name = "حوت"

    # fifth, find the expense ratio between 2 last months
    last_month_in_hijri = int(current_month_in_hijri) - 1

    last_month_expenses = Expense.objects.filter(exp_date__month=str(last_month_in_hijri))

    

    # finally, calculate the total amount, the paid amount, remain amount, and the expense ratio based on previous month
    total = 0
    paid_amount = 0
    remain_amount = 0
    for exp in expenses:
        total += exp.total
        paid_amount += exp.paid_amount
        remain_amount += exp.remain_amount
    last_month_total_expense = 0

    for exp in last_month_expenses:
        last_month_total_expense += exp.total


    percentage = 0
    if last_month_total_expense == 0:
        percentage = 100
    elif last_month_total_expense == total:
        percentage = 0
    else:
        percentage = (last_month_total_expense - total) / total * 100
    
    
    context = {
        "expenses" : expenses,
        "current_month_in_hijri" : current_month_in_hijri, 
        "total" : total, 
        "paid_amount" : paid_amount, 
        "remain_amount" : remain_amount, 
        'month_name' : month_name, 
        "percentage" : percentage
    }

    return render(request, "base/expenses/monthly.html", context)



# weekly expenses report
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def weekly_expenses_view(request):
    date = my_time.date.today()
    date_in_hijri = date2jalali(date)
    start_week = date_in_hijri - my_time.timedelta(date_in_hijri.weekday())
    end_week = start_week + my_time.timedelta(7)
    
    # first, get the current date and time
    now = datetime.now()
    # second, change it to hijri date and get the month
    month = date2jalali(now).month
    # third, find the number of week
    current_week = month * 4.28
    """
        as we know every month is about 4.28 week, so we want to round up this number and get 5
    """
    current_week =my_time.datetime.today().weekday()
    if current_week == 1:
        last_week = 12
    else:
        last_week =  current_week - 1
    # fourth, get all the expenses happened in this week

    expenses = Expense.objects.filter(exp_date__range=[str(start_week), str(end_week)])
    # fifth, calculate the total amount, paid, and remain amount as well as the percentage of ratio 
    
    total = 0
    paid_amount = 0
    remain_amount = 0
    percentage = 0
    for exp in expenses:
        total += exp.total
        remain_amount += exp.remain_amount
        paid_amount += exp.paid_amount
    # get expenses happened in last week
    last_week_expenses = Expense.objects.filter(exp_date__week=last_week)
    last_week_total_expenses = 0
    for exp in last_week_expenses:
        last_week_total_expenses += exp.total
    
    # finally, calculate the percentage
    if last_week_total_expenses == 0 and total > 0:
        percentage = 100
    elif last_week_total_expenses == total:
        percentage = 0
    else:
        percentage = (last_week_total_expenses - total)/total * 100
    context = {
        "expenses" : expenses, 
        "percentage" : percentage, 
        "total" : total,
        "paid_amount" : paid_amount, 
        "remain_amount" : remain_amount
    }

    return render(request, "base/expenses/weekly.html", context)



# get today's expenses
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def today_expense_view(request):
    # get the current date
    now = datetime.now()

    # change it to hijri
    today = date2jalali(now).day
    # get expenses
    expenses = Expense.objects.filter(exp_date__day=today)
    # calculate
    total = 0
    paid_amount = 0
    remain_amount = 0
    percentage = 0
    for exp in expenses:
        total += exp.total
        remain_amount += exp.remain_amount
        paid_amount += exp.paid_amount
    
    # yesterday's expense
    # get yesterday
    if today == 1:
        yesterday = 1
    else:
        yesterday = today - 1

    yesterday_expenses = Expense.objects.filter(exp_date__day=yesterday)
    yesterday_total_expenses = 0
    for exp in yesterday_expenses:
        yesterday_total_expenses += exp.total
    
    if yesterday_total_expenses == 0 and total > 0:
        percentage = 100
    elif yesterday_total_expenses == total:
        percentage = 0
    else:
        percentage = (yesterday_total_expenses - total) / total *100
    
    context = {
        "expenses" : expenses, 
        "percentage" : percentage, 
        "total" : total,
        "paid_amount" : paid_amount, 
        "remain_amount" : remain_amount
    }

    return render(request, "base/expenses/daily.html", context)


# import expense reports



def yearly_report_export(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({"bold" : True})
    money = workbook.add_format({"num_format" : "$#, ##0"})
    date_format = workbook.add_format({"num_format" : "YYYY-MM-dd"})
    # data header
    worksheet.write('A1', 'نمبر', bold)
    worksheet.write('B1', 'عنوان مصرف', bold)
    worksheet.write('C1', 'تاریخ مصرف', bold)
    worksheet.write('D1', 'مقدار مصرف', bold)
    worksheet.write('E1', 'پرداخت شده', bold)
    worksheet.write('F1', 'باقی مانده', bold)
    
    expenses = (
        ["1", "معاش کارمندان", "1400-01-20", 20000, 20000, 0],
        ["2", "معاش کارمندان", "1400-01-20", 20000, 20000, 0],
        ["3", "معاش کارمندان", "1400-01-20", 20000, 20000, 0],
        ["4", "معاش کارمندان", "1400-01-20", 20000, 20000, 0],
        ["5", "معاش کارمندان", "1400-01-20", 20000, 20000, 0]
    )
    
    row = 1
    col = 0

    
    
    workbook.close()


    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="some_file_name.xlsx"'
    # put the spreadsheet data into the response
    response.write(output.getvalue())
    # return the response
    return response



