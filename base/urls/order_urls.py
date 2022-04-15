from django.urls import path
from base.views import order_views


urlpatterns = [
    path("order/<str:pk>/create/", order_views.order_create_view, name="create-order")
]