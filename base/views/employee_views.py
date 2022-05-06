from decimal import Decimal
from django.shortcuts import redirect, render
from base.models import Employee, EmployeeAttendance, EmployeeFee, EmployeeType, OrderDetail, Expense, ExpenseCategory
from django.contrib import messages
from base.forms.employee_forms import EmployeeForm
from datetime import datetime
from jalali_date import date2jalali, datetime2jalali
from users.decorators import allowed_groups
from django.contrib.auth.decorators import login_required


# employee list
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def employee_list(request):
    employees = Employee.objects.all()

    context = {
        "employees" : employees
    }
    return render(request, "base/employees/list.html", context)


# create employee
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def create_employee_view(request):

    if request.method == 'POST':
        emp_type, created = EmployeeType.objects.get_or_create(name=request.POST.get("emp_type"))
        name = request.POST.get("name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        salary_type = request.POST.get("emp_salary_type")
        if salary_type == "month":
            salary_type = "ماهوار"
        elif salary_type == 'kontorat':
            salary_type = "کونترات"

        address = request.POST.get("address")
        salary = request.POST.get("salary")
        if salary == "":
            salary = None

        obj = Employee.objects.create(
            emp_type=emp_type, 
            first_name=name, 
            last_name=last_name,
            phone_number=phone_number, 
            salary_per_month=salary, 
            address=address, 
            salary=salary_type
        )

        if obj:
            messages.success(request, "کارمند جدید موفقانه ثبت گردید.")
            return redirect("employee-create")
        else:
            messages.error(request, "مشکلی رخ داد، لطفا دوباره تلاش کنید. ")
            return redirect("employee-create")

    
    return render(request, "base/employees/create.html")

# update employee
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def employee_update_view(request, pk):
    employee = Employee.objects.get(pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "کارمند فوق موفقانه ویرایش گردید. ")
            return redirect("employee-list")
    else:
        form = EmployeeForm(instance=employee)
    
    context = {
        "form" : form
    }
    return render(request, "base/employees/update.html", context)


# delete employee
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def employee_delete_view(request):
    if request.method == "POST":
        emp = Employee.objects.get(id=request.POST.get("employee"))
        if emp.employeefee_set.exists():
            messages.error(request, "شما نمیتوانید کارمند ذیل را حذف کنید.")
            return redirect("employee-list")
        else:
            emp.delete()
            messages.success(request, "کارمند ذیل موفقانه از سیستم حذف گردید. ")
            return redirect("employee-list")


# employee detail
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def employee_detail_view(request, pk):
    employee = Employee.objects.get(pk=pk)
    works = employee.employeefee_set.all()

    context = {
        "employee" : employee, 
        "works" : works
    }

    return render(request, "base/employees/detail.html", context)


# employee get salary
@login_required(login_url="login")
@allowed_groups(groups=['admin'])
def employee_get_salary_view(request):
    now = datetime.now()
    # get it in hijri
    hijri = date2jalali(now).strftime("%Y-%m-%d")
    if request.method == "POST":
        ef = EmployeeFee.objects.get(pk=request.POST.get("employee_fee"))
        amount = request.POST.get("amount")
        category = ExpenseCategory.objects.get(category_name="معاشات کارمندان")
        try:
            Expense.objects.create(
                category = category,
                exp_amount = Decimal(amount),
                exp_date = hijri, 
                exp_quantity = Decimal(1),
                alternative = Decimal(1),
                paid_amount = Decimal(amount), 
                price_unit = "افغانی"
            )
            ef.get_amount += Decimal(amount)
            ef.remain_amount = Decimal(ef.remain_amount) - Decimal(amount)
            ef.save()
            messages.success(request, "پرداختی موفقانه انجام شد. ")
            return redirect("employee-detail", ef.employee.id)
        except:
            messages.error(request, "اشتباه رخ داد لطفا دوباره تلاش کنید. ")
            return redirect("employee-detail", ef.employee.id)




# employee attendance
def employee_attendance_view(request, pk):

    employee = Employee.objects.get(pk=pk)
    attnedances = employee.employeeattendance_set.all()
    if request.method == "POST":
        status = request.POST.get("status")
        if status == "present":
            status = "حاضر"
        elif status == "absent":
            status = "غیر حاضر"
        elif status == "late":
            status = "تاخیر بیش از یک ساعت"
        print(status)
        penalty = request.POST.get("penalty")
        print(penalty)
        date = request.POST.get("date")
        print(date)
        
        try:
            EmployeeAttendance.objects.create(
                employee=employee, 
                status=status, 
                penalty_percentage=penalty, 
                date=date
            )
            messages.success(request, "عملیات موفقانه انجام شد. ")
            
        except:
            messages.error(request, "مشکلی رخ داد، لطفا چک کرده و دوباره تلاش کنید. ")
        return redirect("employee-attendance", employee.id)
    context = {
        "employee" : employee, 
        "attnedances" :attnedances
    }
    return render(request, "base/employees/attendance.html", context)
