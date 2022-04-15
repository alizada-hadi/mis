from django.db import models

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=100)
    social_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"



class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.customer.first_name}'s order"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    DIRECTION = (
        ("راست", "راست"),
        ("چپ", "چپ"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قد", null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="بر", null=True, blank=True)
    depth = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="عمق", null=True, blank=True)
    direction = models.CharField(max_length=30, choices=DIRECTION, default="راست", null=True,  blank=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="مقدار / تعداد")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="قیمت فی واحد")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مجموع")
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مقدار پرداخت شده")
    remain_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="مقدار باقی مانده")
    type = models.CharField(max_length=200, verbose_name="نوعیت کار")

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.order.quantity * self.price
        if not self.remain_amount:
            self.remain_amount = self.total - self.paid_amount
    
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.order}'s detail "