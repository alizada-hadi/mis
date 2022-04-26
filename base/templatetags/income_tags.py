from django import template
from base.models import Income, Expense
from datetime import datetime
from jalali_date import date2jalali


register = template.Library()

# annual total income
@register.simple_tag
def annual_total_income(year):
    incomes = Income.objects.filter(recieved_at__year=year)
    total = 0
    for income in incomes:
        total += income.total

    return total

# annual total income and compare it with last year in percentag
@register.simple_tag
def income_ratio(current_year, last_year):
    current_year_incomes = Income.objects.filter(recieved_at__year=current_year)
    last_year_incomes = Income.objects.filter(recieved_at__year=last_year)
    current_year_total_income = 0
    last_year_total_income = 0
    for i in current_year_incomes:
        current_year_total_income += i.total
    for j in last_year_incomes:
        last_year_total_income += j.total
    
    percentage = 0
    # formula = last - new / new * 100
    if last_year_total_income == 0:
        percentage = 100
    elif last_year_total_income == current_year_total_income:
        percentage = 0
    else:
        percentage = (last_year_total_income - current_year_total_income) / current_year_total_income * 100

    return percentage

# copare it with this year expense
@register.simple_tag
def income_expense_comparision(year):
    incomes = Income.objects.filter(recieved_at__year=year)
    expenses = Expense.objects.filter(exp_date__year=year)

    total_income = 0
    total_expense = 0

    for i in incomes:
        total_income += i.total
    for j in expenses:
        total_expense += j.total

    percentage = 0

    percentage = total_expense / total_income * 100
    percentage = round(percentage, 2)
    return percentage


@register.simple_tag
def monthly_total_income(month):
    incomes = Income.objects.filter(recieved_at__month=month)
    total = 0
    for i in incomes:
        total += i.total
    
    return total

@register.simple_tag
def monthly_income_ratio(current_month, last_month):
    current_month_incomes = Income.objects.filter(recieved_at__month=current_month)
    last_month_incomes = Income.objects.filter(recieved_at__month=last_month)
    current_month_total_income = 0
    last_month_total_income = 0
    for i in current_month_incomes:
        current_month_total_income += i.total
    for j in last_month_incomes:
        last_month_total_income += j.total
    
    percentage = 0
    # formula = last - new / new * 100
    if last_month_total_income == 0:
        percentage = 100
    elif last_month_total_income == current_month_total_income:
        percentage = 0
    else:
        percentage = (last_month_total_income - current_month_total_income) / current_month_total_income * 100

    return percentage

@register.simple_tag
def monthly_income_comparision(month):
    incomes = Income.objects.filter(recieved_at__month=month)
    expenses = Expense.objects.filter(exp_date__month=month)

    total_income = 0
    total_expense = 0

    for i in incomes:
        total_income += i.total
    for j in expenses:
        total_expense += j.total

    percentage = 0

    percentage = total_expense / total_income * 100
    percentage = round(percentage, 2)
    return percentage


# daily

@register.simple_tag
def daily_total_income(day):
    incomes = Income.objects.filter(recieved_at__day=day)
    total = 0
    for i in incomes:
        total += i.total
    
    return total

@register.simple_tag
def daily_income_ratio(today, yesterday):
    today_incomes = Income.objects.filter(recieved_at__day=today)
    yesterday_incomes = Income.objects.filter(recieved_at__day=yesterday)
    today_total_income = 0
    yesterday_total_income = 0
    for i in today_incomes:
        today_total_income += i.total
    for j in yesterday_incomes:
        yesterday_total_income += j.total
    
    percentage = 0
    # formula = last - new / new * 100
    if yesterday_total_income == 0:
        percentage = 100
    elif today_total_income == yesterday_total_income:
        percentage = 0
    elif today_total_income == 0:
        percentage = 0
    else:
        percentage = (yesterday_total_income - today_total_income) / today_total_income * 100
    percentage = round(percentage, 2)
    if yesterday_total_income > today_total_income:
        percentage = -percentage
    return percentage

@register.simple_tag
def daily_income_comparision(day):
    incomes = Income.objects.filter(recieved_at__day=day)
    expenses = Expense.objects.filter(exp_date__day=day)

    total_income = 0
    total_expense = 0

    for i in incomes:
        total_income += i.total
    for j in expenses:
        total_expense += j.total
    
    

    percentage = 0

    if total_expense == 0 and total_income == 0:
        percentage = 0
    elif total_expense == 0 and total_income > 0:
        percentage = 100
    elif total_expense > 0 and total_income == 0:
        percentage = 0
    else:
        percentage = total_expense / total_income * 100
    percentage = round(percentage, 2)
    return percentage