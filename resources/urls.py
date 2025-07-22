from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    # หน้าหลัก - รายการหนังสือทั้งหมด
    path('', views.book_list, name='list'),
    
    # รายละเอียดหนังสือ
    path('book/<int:pk>/', views.book_detail, name='detail'),
    
    # กรองตามประเภท
    path('type/<int:type_id>/', views.book_by_type, name='by_type'),
    
    # กรองตามหมวดเรื่อง
    path('subject/<int:subject_id>/', views.book_by_subject, name='by_subject'),
    
    # ค้นหา
    path('search/', views.book_search, name='search'),
    
    # รายการแนะนำ
    path('featured/', views.featured_books, name='featured'),
]