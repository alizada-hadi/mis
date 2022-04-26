from django.urls import path
from base.views import income_views
urlpatterns = [
    path("incomes/list/", income_views.income_list_view, name="income-list"), 
    path("income/create/", income_views.income_create_view, name="income-create"), 
    path("income/annual/report/", income_views.income_annual_report, name="income-annual-report"), 
    path("income/monthly/report/", income_views.monthly_income_report, name="income-monthly-report"), 
    path("income/weekly/report/", income_views.weekly_income_report, name="weekly-income-report"), 
    path("income/daily/report/", income_views.daily_income_report, name="daily-income-report")
]
