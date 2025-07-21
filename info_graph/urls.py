# info_graph/urls.py
from django.urls import path,include
from info_graph import views

urlpatterns = [
    path('', views.view_graph, name='view_graph'),
    # เพิ่ม URLs สำหรับหน้ารายละเอียด
    path('greenhouse/', views.greenhouse_detail, name='greenhouse_detail'),
    path('electricity/', views.electricity_detail, name='electricity_detail'),
    path('diesel/', views.diesel_detail, name='diesel_detail'),
    path('water/', views.water_detail, name='water_detail'),
    path('landfill/', views.landfill_detail, name='landfill_detail'),
    path('paper/', views.paper_detail, name='paper_detail'),
]