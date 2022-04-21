from django.contrib import admin
from .models import Customer, Category, Order, OrderDetail, Employee, Recieve, EmployeeType, EmployeeFee
# Register your models here.


admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Employee)
admin.site.register(Recieve)
admin.site.register(EmployeeType)
admin.site.register(EmployeeFee)
