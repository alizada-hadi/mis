from django.urls import path
from base.views import customer_views, exhibition_views

urlpatterns = [
    path("customer/list/", customer_views.customer_list_view, name="customer-list"), 
    path("customer/create/", customer_views.customer_create_view, name="create-customer"),
    path("customer/update/", customer_views.update_customer, name="update-customer"), 
    path('customer/delete/', customer_views.customer_delete_view, name="customer-delete"), 

    path("customer/list/mine/", exhibition_views.my_customers, name="my-customer"), 
    path("customer/create/mine/", exhibition_views.create_new_customer, name="mine-customer-create"), 
    path("customer/detail/mine/<str:pk>/", exhibition_views.my_customer_detail, name="mine-customer-detail"), 


    # exhibition list
    path("exhibitions/list/", exhibition_views.exhibition_list_create_view, name="exhibition-list")
]