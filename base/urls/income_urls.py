from django.urls import path
from base.views import income_views
urlpatterns = [
    path("incomes/list/", income_views.income_list_view, name="income-list"), 
    path("income/create/", income_views.income_create_view, name="income-create"), 
    path("income/annual/report/", income_views.income_annual_report, name="income-annual-report")
]
