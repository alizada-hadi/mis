from atexit import register
from django import template
from base.models import Employee, Expense, Income, Order
from datetime import datetime
from jalali_date import date2jalali


register = template.Library()

# calculate total expenses in a given year
@register.simple_tag
def annual_total_expense(year):
    expenses = Expense.objects.filter(exp_date__year=year)
    total = 0
    for exp in expenses:
        total += exp.total
    
    return total


@register.simple_tag
def annual_total_income(year):
    incomes = Income.objects.filter(recieved_at__year=year)
    total = 0
    for i in incomes:
        total += i.total
    
    return total


@register.simple_tag
def annual_total_order(year):
    orders = Order.objects.filter(date_ordered__year=year).count()
    return orders

@register.simple_tag
def number_of_employees():
    return Employee.objects.all().count()
