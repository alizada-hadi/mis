from django.urls import path
from base.views import employee_views


urlpatterns = [
    path("employee/list/", employee_views.employee_list, name="employee-list"), 
    path("employee/create/", employee_views.create_employee_view, name="employee-create"), 
    path("employee/update/<str:pk>/", employee_views.employee_update_view, name="employee-update"), 
    path("employee/delete/", employee_views.employee_delete_view, name="employee-delete"), 
    path("employee/detail/<str:pk>/", employee_views.employee_detail_view, name="employee-detail"),
    path("employee/get/salary/", employee_views.employee_get_salary_view, name="employee-get-salary")

]