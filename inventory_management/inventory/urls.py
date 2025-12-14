
from django.urls import path
from .import views

urlpatterns = [
    path('', views.startup_view, name='home'),
    path('adminLogin/', views.admin_login_view, name='adminLogin'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('inventoryhome/', views.inventoryhome_view, name='inventoryhome'), 
    path('assemblyform/', views.assembly_view, name='assemblyform'),
    path('exhardForm/', views.exhardForm_view, name='exhardForm'),
    path('download_excel/', views.download_excel, name='download_excel'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    
]




