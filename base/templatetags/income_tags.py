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