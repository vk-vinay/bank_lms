from django.contrib import admin
from django.urls import path

from bank import views as bank_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping/", bank_views.ping),
    path("deposit/", bank_views.deposit),
    path("withdraw/", bank_views.withdraw),
    path("transfer/", bank_views.transfer),
    path("report/", bank_views.report),
]
