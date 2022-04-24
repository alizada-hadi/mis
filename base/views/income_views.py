from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from base.models import Income
from datetime import datetime
from jalali_date import date2jalali


# income list
def income_list_view(request):
    object_list = Income.objects.all()

    context = {
        "incomes" : object_list
    }
    return render(request, "base/incomes/list.html", context)


# create income
def income_create_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        amount = request.POST.get("amount")
        unit = request.POST.get("unit")
        if unit == "afg":
            unit = "افغانی"
        elif unit == "usd":
            unit = "دالر"
        elif unit == "kaldar":
            unit = "کلدار"
        elif unit == "toman":
            unit = "تومان"
        alternative = request.POST.get("alternative")
        if not alternative:
            alternative = Decimal(1)
        date = request.POST.get("date")

        try:
            Income.objects.create(
                income_title=title, 
                amount = Decimal(amount), 
                price_unit=unit, 
                alternative=alternative, 
                recieved_at=date
            )
            messages.success(request, "مورد جدید موفقانه  ثبت سیستم گردید. ")
        except:
            messages.error(request, "مشکلی رخ داد لطفا چک کرده و دوباره تلاش کنید. ")

        return redirect("income-list")    


# filter the income based on year, month, week, and day

def income_annual_report(request):
    # first, get the date
    now = datetime.now()
    # second, change date to hijri
    current_year = date2jalali(now).strftime("%Y")
    last_year = int(current_year) - 1
    last_year = str(last_year)
    # third, filter the income based on current year
    incomes = Income.objects.filter(recieved_at__year=current_year)


    context = {
        "incomes" : incomes, 
        "current_year" : current_year, 
        "last_year" : last_year
    }

    return render(request, "base/incomes/annual.html", context)



