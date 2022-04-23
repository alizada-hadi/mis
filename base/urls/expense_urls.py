from django.urls import path
from base.views import expense_views

urlpatterns = [
    path("expenses/all/", expense_views.expense_list_view, name="expense-list"), 
    path("expense/create/", expense_views.create_expense_view, name="create-expense"), 
    path("expense/delete/", expense_views.delete_expense_view, name="expense-delete"), 
    path("expense/detail/<str:pk>/", expense_views.expense_detail_view, name="expense-detail"), 
    path("expense/annual/report/",  expense_views.annual_expense_view, name="expense-annual")
]