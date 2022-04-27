from django.shortcuts import render, get_object_or_404, redirect
from base.models import *
from django.contrib import messages
from datetime import datetime
from jalali_date import date2jalali
from users.decorators import allowed_groups
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def dashboard(request):
    labels = []
    data = {
        "income" : [], 
        "expense" : [], 
        "date" : []
    }
    order_data = {
        "number_of_order" : [], 
        "month" : []
    }
    now = datetime.now()
    current_year = date2jalali(now).strftime("%Y")
    
    expenses = Expense.objects.all().order_by("exp_date")
    incomes = Income.objects.all().order_by("recieved_at")
    for exp in expenses:
        data["expense"].append(int(exp.total))
        data["date"].append(exp.exp_date.strftime("%Y-%m-%d"))

    for i in incomes:
        data["income"].append(int(i.total))
        data["date"].append(i.recieved_at.strftime("%Y-%m-%d"))
    
    for i in range(1, 13):
        order_data['number_of_order'].append(Order.objects.filter(date_ordered__month=i).count())
        if i == 1:
            order_data['month'].append("حمل")
        elif i == 2:
            order_data['month'].append("ثور")
        elif i == 3:
            order_data['month'].append("جوزا")
        elif i == 4:
            order_data['month'].append("سرطان")
        elif i == 5:
            order_data['month'].append("اسد")
        elif i == 6:
            order_data['month'].append("سنبله")
        elif i == 7:
            order_data['month'].append("میزان")
        elif i == 8:
            order_data['month'].append("عقرب")
        elif i == 9:
            order_data['month'].append("قوس")
        elif i == 10:
            order_data['month'].append("جدی")
        elif i == 11:
            order_data['month'].append("دلو")
        elif i == 12:
            order_data['month'].append("حوت")
    context = {
        "current_year" : current_year, 
        "labels" : labels, 
        "data" : data, 
        "order_data" : order_data
    }

    return render(request, "base/dashboards/index.html", context)
