
from django.contrib import admin
from django.urls import path, include
from . import  views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index), 
    path("", include("base.urls.customer_urls")),
    path("", include("base.urls.order_urls")),
]
