from django import views
from django.urls import path
from base.views import order_views


urlpatterns = [
    path("order/<str:pk>/create/", order_views.order_create_view, name="create-order"), 
    path("order/<str:pk>/detail/", order_views.order_detail_view, name="order-detail"),
    path("order/<str:pk>/update/", order_views.order_update_view, name="update-order"), 

    path("order/<str:pk>/emp/pdf/", order_views.employee_generate_pdf, name="employee-order-pdf"), 
    path("order/<str:pk>/customer/pdf/", order_views.customer_generate_pdf, name="customer-order-pdf"), 
    path("recieve/create/", order_views.recieve_view, name="add-recieve"), 
    path("recieve/<str:pk>/list/", order_views.recieve_list_view, name="recieve-list"), 
    path("order_detail/<str:pk>/add_employee/", order_views.employee_work_view, name="add-employee"), 
    path("order/delete/", order_views.order_delete_view, name="order-delete"), 
    path("order/detail/delete/", order_views.order_detail_delete, name="order-detail-delete")
]