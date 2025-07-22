from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import PromotionalCategory, PromotionalImage


def promotional_list(request):
    """หน้าแสดงรายการหมวดหมู่สื่อประชาสัมพันธ์"""
    categories = PromotionalCategory.objects.filter(is_active=True).prefetch_related('images')
    
    # เพิ่มข้อมูลรูปภาพเด่นสำหรับแต่ละหมวดหมู่
    for category in categories:
        category.featured_images = category.images.filter(is_active=True, is_featured=True)[:5]
        category.latest_images = category.images.filter(is_active=True).order_by('display_order', '-created_at')[:10]
    
    context = {
        'categories': categories,
        'page_title': 'สื่อประชาสัมพันธ์'
    }
    return render(request, 'promotional/list.html', context)


def promotional_category(request, category_id):
    """หน้าแสดงรูปภาพในหมวดหมู่"""
    category = get_object_or_404(PromotionalCategory, id=category_id, is_active=True)
    
    # ดึงรูปภาพในหมวดหมู่
    images_list = PromotionalImage.objects.filter(
        category=category, 
        is_active=True
    ).order_by('display_order', '-created_at')
    
    # แบ่งหน้า
    paginator = Paginator(images_list, 12)  # 12 รูปต่อหน้า
    page_number = request.GET.get('page')
    images = paginator.get_page(page_number)
    
    # รูปภาพเด่น
    featured_images = images_list.filter(is_featured=True)[:6]
    
    context = {
        'category': category,
        'images': images,
        'featured_images': featured_images,
        'page_title': f'สื่อประชาสัมพันธ์ - {category.name_th}'
    }
    return render(request, 'promotional/category.html', context)


def promotional_gallery(request):
    """หน้าแสดงรูปภาพทั้งหมดแบบ gallery"""
    
    # Filter
    category_id = request.GET.get('category')
    tag = request.GET.get('tag')
    
    images_list = PromotionalImage.objects.filter(is_active=True)
    
    if category_id:
        images_list = images_list.filter(category_id=category_id)
    
    if tag:
        images_list = images_list.filter(tags__icontains=tag)
    
    images_list = images_list.order_by('-is_featured', 'display_order', '-created_at')
    
    # แบ่งหน้า
    paginator = Paginator(images_list, 15)  # 15 รูปต่อหน้า
    page_number = request.GET.get('page')
    images = paginator.get_page(page_number)
    
    # สำหรับ filter
    categories = PromotionalCategory.objects.filter(is_active=True)
    
    # แท็กยอดนิยม
    all_images = PromotionalImage.objects.filter(is_active=True, tags__isnull=False).exclude(tags='')
    popular_tags = []
    for img in all_images:
        popular_tags.extend(img.tag_list)
    popular_tags = list(set(popular_tags))[:10]  # 10 แท็กแรก
    
    context = {
        'images': images,
        'categories': categories,
        'popular_tags': popular_tags,
        'selected_category': category_id,
        'selected_tag': tag,
        'page_title': 'แกลเลอรี่สื่อประชาสัมพันธ์'
    }
    return render(request, 'promotional/gallery.html', context)