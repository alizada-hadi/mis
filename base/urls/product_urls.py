from django.urls import path
from base.views import product_views


urlpatterns = [
    path("products/list/", product_views.product_list_create_view, name="product-list"),
    path("product/<str:pk>/detail/", product_views.product_detail_view, name="product-detail"), 
    path("product/<str:pk>/update/", product_views.product_update_view, name="product-update"), 
    path("product/delete/", product_views.delete_product_view, name="product-delete")
]
