from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
