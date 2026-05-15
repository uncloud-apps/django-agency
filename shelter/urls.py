from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('servers/', views.server_list, name='server_list'),
    path('servers/<slug:slug>/', views.server_detail, name='server_detail'),
    path('servers/<slug:slug>/apply/', views.apply, name='apply'),
    path('applications/<uuid:pk>/', views.application_status, name='application_status'),
]
