from django.forms import ModelForm
from base.models import Employee


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = [
            "emp_type" ,
            "first_name", 
            "last_name", 
            "address", 
            "phone_number", 
            "salary",
            "salary_per_month"
        ]


