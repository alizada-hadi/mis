
from django.contrib import admin
from django.urls import path, include
from . import  views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("base.urls.customer_urls")),
    path("", include("base.urls.order_urls")),
    path("", include("base.urls.employee_urls")), 
    path("", include("base.urls.expense_urls")),
    path("", include("base.urls.income_urls")),
    path("", include("base.urls.dashboard_urls")),

    path("", include("users.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
