from django.urls import path
from . import views

urlpatterns = [
    path("create_order", views.CreateOrder.as_view()),
]
