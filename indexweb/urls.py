from django.urls import path
from indexweb import views

urlpatterns = [
    path('', views.index, name='index'),
]