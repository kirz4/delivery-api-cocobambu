from django.urls import path
from . import views

urlpatterns = [
    path("orders/", views.list_orders),
    path("orders/<str:order_id>/", views.get_order),
]