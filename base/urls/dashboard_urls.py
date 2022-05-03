from django.urls import path
from base.views import dashboard_views

urlpatterns = [
    path("", dashboard_views.dashboard, name="dashboard"), 
    path("manager/user/", dashboard_views.manager_dashboard, name="manager-dashboard")
]
