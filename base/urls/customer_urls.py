from django.urls import path
from base.views import customer_views

urlpatterns = [
    path("customer/list/", customer_views.customer_list_view, name="customer-list"), 
    path("customer/create/", customer_views.customer_create_view, name="create-customer"),
    path("customer/update/", customer_views.update_customer, name="update-customer"), 
    path('customer/delete/', customer_views.customer_delete_view, name="customer-delete")
]