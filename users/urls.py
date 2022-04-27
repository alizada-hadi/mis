from django.urls import path
from . import views

urlpatterns = [
    path("account/register/", views.user_register_view, name="register"), 
    path("account/login/", views.user_login_view, name="login"), 
    path("account/logout/", views.user_logout_view, name="logout"),
    path("account/unauthorize/", views.unauthorize_view, name="unauthorize")
]
