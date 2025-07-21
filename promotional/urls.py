from django.urls import path
from . import views

app_name = 'promotional'

urlpatterns = [
    path('', views.promotional_list, name='list'),
    path('category/<int:category_id>/', views.promotional_category, name='category'),
    path('gallery/', views.promotional_gallery, name='gallery'),
]