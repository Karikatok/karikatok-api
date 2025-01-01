from django.urls import path

from . import views

urlpatterns = [
    path("login", views.Login.as_view()),
    path("signup", views.Signup.as_view()),
    path("create_account", views.CreateAccount.as_view()),
]