from django.urls import path
from greenweb import views

urlpatterns = [
    path('', views.index2, name='index2'),
    path('year/<int:selected_year>/', views.index2, name='index2_year'),
    path('ajax/chart-data/<int:year>/', views.get_chart_data_ajax, name='chart_data_ajax'),
    path('view_pdf/<path:id_pdf>', views.view_pdf, name='view_pdf'),
    path('view_pdf_doc/<path:id_pdf>', views.view_pdf_doc, name='view_pdf_doc'),
    path('view_category/', views.view_category, name='view_category'),
    path('view_document/', views.view_document, name='view_document'),
    path('view_promotional/', views.view_promotional, name='view_promotional'), 
    path('blog_detail/<int:pk>', views.blog_detail, name='blog_detail'),
    path('blog_list/', views.blog_list, name='blog_list'),
    path('view_group/<str:group_name>', views.view_group, name='view_group'),
    path('view_group/<str:group_name>/<str:year_name>', views.view_group, name='view_group_year'),
]
