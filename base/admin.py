from django.contrib import admin
from .models import Customer, Category, Order, OrderDetail
# Register your models here.


admin.site.register(Customer)
admin.site.register(Category)


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ["category", "customer", "date_ordered"]
    inlines = [OrderDetailInline]