from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Exhibition(models.Model):
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name



class Customer(models.Model):
    # add_by = models.ForeignKey(Exhibition, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=100)
    social_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class EmployeeType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    SALARY =  (
        ("ماهوار", "ماهوار"),
        ("کونترات", "کونترات"),
    )
    emp_type = models.ForeignKey(EmployeeType, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    salary = models.CharField(max_length=20, choices=SALARY)
    salary_per_month = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class EmployeeAttendance(models.Model):
    STATUS = (
        ("حاضر", "حاضر"), 
        ("غایب", "غایب"), 
        ("تاخیر بیش از یک ساعت", "تاخیر بیش از یک ساعت"), 
    )
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="حاضر")
    penalty_percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.employee.first_name}'s attendance "



class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="product/images", default="product.jpg")

    def __str__(self):
        return self.name



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مقدار پرداخت شده", null=True, blank=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    date_ordered = models.DateField()


    def __str__(self):
        return f"{self.customer.first_name}'s order"


class Recieve(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    amount_letter = models.CharField(max_length=200)
    recived_at = models.DateField()

    def __str__(self):
        return f"recieve from {self.order.id}"


class OrderDetail(models.Model):
    DIRECTION = (
        ("راست", "راست"),
        ("چپ", "چپ"),
    )
    PRICE_UNIT = (
        ("افغانی", "افغانی"), 
        ("دالر",  "دالر"),
        ("کلدار",  "کلدار"),
        ("تومان",  "تومان"),
    )
    WITH_COLOR = (
        ("بلی", "بلی"), 
        ("نخیر",  "نخیر"),
    )
    CHOICES = (
        ("رنگ",  "رنگ"),
        ("واکیوم",  "واکیوم"),
    )
    OPTIONS = (
        ("بلی", "بلی"), 
        ("نخیر",  "نخیر"),
    )
    UNIT = (
        ("عدد", "عدد"), 
        ("متر",  "متر"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قد", null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="بر", null=True, blank=True)
    depth = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="عمق", null=True, blank=True)
    direction = models.CharField(max_length=30, choices=DIRECTION, default="راست", null=True,  blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مقدار / تعداد")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="قیمت فی واحد")
    price_unit = models.CharField(max_length=20, choices=PRICE_UNIT)
    alternative = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vacum = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مجموع")
    remain_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مقدار باقی مانده")
    with_color =  models.CharField(max_length=20, choices=WITH_COLOR, null=True, blank=True)
    type = models.CharField(max_length=200, verbose_name="نوعیت کار")

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.quantity * (self.price * self.alternative)
        if not self.remain_amount:
            self.remain_amount = self.total - self.order.paid_amount
    
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.order}'s detail "



class EmployeeFee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,  null=True)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.SET_NULL, null=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    get_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    remain_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.employee.first_name}'s work "

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = Decimal(self.order_detail.quantity) * Decimal(self.fee)

        if not self.remain_amount:
            self.remain_amount = Decimal(self.total_amount )- Decimal(self.get_amount)

        super().save(*args, **kwargs)



# expense and income
class ExpenseCategory(models.Model):
    category_name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.category_name

class Expense(models.Model):
    PRICE_UNIT = (
        ("افغانی", "افغانی"), 
        ("دالر",  "دالر"),
        ("کلدار",  "کلدار"),
        ("تومان",  "تومان"),
    )
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    good_name = models.CharField(max_length=200, null=True, blank=True)
    rant_month = models.DateField(null=True, blank=True)
    from_place = models.CharField(max_length=200, null=True, blank=True)
    to_place = models.CharField(max_length=200, null=True, blank=True)
    exp_quantity =  models.DecimalField(max_digits=8, decimal_places=2, default=1)
    exp_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    price_unit = models.CharField(max_length=20, choices=PRICE_UNIT, default="افغانی")
    alternative = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    exp_date = models.DateField()
    exp_description = models.TextField(null=True, blank=True)

    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    remain_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)


    def __str__(self) -> str:
        return f"{self.category} expense "

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.exp_quantity * (self.exp_amount * self.alternative)
        if not self.remain_amount:
            self.remain_amount = self.total - self.paid_amount
    
        super().save(*args, **kwargs)


class Income(models.Model):
    PRICE_UNIT = (
        ("افغانی", "افغانی"), 
        ("دالر",  "دالر"),
        ("کلدار",  "کلدار"),
        ("تومان",  "تومان"),
    )
    income_title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    price_unit = models.CharField(max_length=20, choices=PRICE_UNIT, default="افغانی")
    alternative = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    recieved_at = models.DateField()
    
    def __str__(self) -> str:
        return self.income_title

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.amount * self.alternative
        super().save(*args, **kwargs)


