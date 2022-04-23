from django import forms
from base.models import Expense
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['exp_date'] = JalaliDateField( label=("تاریخ مصرف"), widget=AdminJalaliDateWidget)