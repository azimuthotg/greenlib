from django.urls import path,include
from info_graph import views

urlpatterns = [
    path('', views.view_graph, name='view_graph'),
]