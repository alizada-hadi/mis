from django.urls import path
from base.views import product_views


urlpatterns = [
    path("products/list/", product_views.product_list_create_view, name="product-list"),
]
