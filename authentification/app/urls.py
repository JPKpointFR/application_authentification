from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name='home'),
    path("register", views.register, name='register'),
    path("login", views.login_, name='login'),
    path("logout", views.logout_, name='logout'),
    path("activate/<uidb64>/<token>", views.activate, name='activate'),
]
