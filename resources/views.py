from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Book, ResourceType, Subject


def book_list(request):
    """หน้าแสดงรายการหนังสือทั้งหมด"""
    
    books = Book.objects.filter(is_active=True, is_available=True).select_related(
        'resource_type', 'subject'
    )
    
    # กรองตามประเภท
    resource_type_id = request.GET.get('type')
    if resource_type_id:
        books = books.filter(resource_type_id=resource_type_id)
    
    # กรองตามหมวดเรื่อง
    subject_id = request.GET.get('subject')
    if subject_id:
        books = books.filter(subject_id=subject_id)
    
    # ค้นหา
    search_query = request.GET.get('q', '').strip()
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(call_number__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # เรียงลำดับ
    books = books.order_by('order_number', 'title')
    
    # แบ่งหน้า
    paginator = Paginator(books, 20)  # 20 รายการต่อหน้า
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # สำหรับ filter
    resource_types = ResourceType.objects.filter(is_active=True)
    subjects = Subject.objects.filter(is_active=True)
    
    # หนังสือแนะนำ
    featured_books = Book.objects.filter(
        is_active=True, 
        is_available=True, 
        is_featured=True
    ).select_related('resource_type')[:6]
    
    context = {
        'page_obj': page_obj,
        'books': page_obj,
        'resource_types': resource_types,
        'subjects': subjects,
        'featured_books': featured_books,
        'search_query': search_query,
        'selected_type': resource_type_id,
        'selected_subject': subject_id,
        'page_title': 'ทรัพยากรสารสนเทศด้านสิ่งแวดล้อม',
        'total_books': paginator.count,
    }
    
    return render(request, 'resources/book_list.html', context)


def book_detail(request, pk):
    """หน้าแสดงรายละเอียดหนังสือ"""
    
    book = get_object_or_404(
        Book.objects.select_related('resource_type', 'subject'),
        pk=pk,
        is_active=True
    )
    
    # หนังสือที่เกี่ยวข้อง (หมวดเรื่องเดียวกัน)
    related_books = Book.objects.filter(
        subject=book.subject,
        is_active=True,
        is_available=True
    ).exclude(pk=book.pk)[:6]
    
    context = {
        'book': book,
        'related_books': related_books,
        'page_title': book.short_title,
    }
    
    return render(request, 'resources/book_detail.html', context)


def book_by_type(request, type_id):
    """หน้าแสดงหนังสือตามประเภท"""
    
    resource_type = get_object_or_404(ResourceType, pk=type_id, is_active=True)
    
    books = Book.objects.filter(
        resource_type=resource_type,
        is_active=True,
        is_available=True
    ).select_related('resource_type', 'subject').order_by('order_number', 'title')
    
    # แบ่งหน้า
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'books': page_obj,
        'resource_type': resource_type,
        'page_title': f'ทรัพยากรประเภท: {resource_type.name}',
        'total_books': paginator.count,
    }
    
    return render(request, 'resources/book_by_type.html', context)


def book_by_subject(request, subject_id):
    """หน้าแสดงหนังสือตามหมวดเรื่อง"""
    
    subject = get_object_or_404(Subject, pk=subject_id, is_active=True)
    
    books = Book.objects.filter(
        subject=subject,
        is_active=True,
        is_available=True
    ).select_related('resource_type', 'subject').order_by('order_number', 'title')
    
    # แบ่งหน้า
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'books': page_obj,
        'subject': subject,
        'page_title': f'หมวดเรื่อง: {subject.name}',
        'total_books': paginator.count,
    }
    
    return render(request, 'resources/book_by_subject.html', context)


def book_search(request):
    """หน้าค้นหาหนังสือ"""
    
    search_query = request.GET.get('q', '').strip()
    books = Book.objects.none()
    
    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(call_number__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(publisher__icontains=search_query),
            is_active=True,
            is_available=True
        ).select_related('resource_type', 'subject').order_by('order_number', 'title')
    
    # แบ่งหน้า
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'books': page_obj,
        'search_query': search_query,
        'page_title': f'ผลการค้นหา: {search_query}' if search_query else 'ค้นหาหนังสือ',
        'total_books': paginator.count,
    }
    
    return render(request, 'resources/book_search.html', context)


def featured_books(request):
    """หน้าแสดงหนังสือแนะนำ"""
    
    books = Book.objects.filter(
        is_active=True,
        is_available=True,
        is_featured=True
    ).select_related('resource_type', 'subject').order_by('order_number', 'title')
    
    # แบ่งหน้า
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'books': page_obj,
        'page_title': 'หนังสือแนะนำ',
        'total_books': paginator.count,
    }
    
    return render(request, 'resources/featured_books.html', context)