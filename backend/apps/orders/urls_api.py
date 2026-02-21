from django.urls import path
from . import views

urlpatterns = [
    path("orders/", views.orders_collection),
    path("orders/<str:order_id>/", views.order_resource),
    path("orders/<str:order_id>/status/", views.change_order_status),
]