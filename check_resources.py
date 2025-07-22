#!/usr/bin/env python
"""
สคริปต์ตรวจสอบข้อมูล Resources
รัน: python check_resources.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webproject.settings')
django.setup()

from resources.models import Book, ResourceType, Subject

def check_data():
    """ตรวจสอบข้อมูลในฐานข้อมูล"""
    
    print("🔍 ตรวจสอบข้อมูล Resources...")
    print("="*50)
    
    # ตรวจสอบ ResourceType
    print(f"📁 ResourceType: {ResourceType.objects.count()} รายการ")
    for rt in ResourceType.objects.all():
        print(f"   - {rt.name} (Active: {rt.is_active})")
    
    # ตรวจสอบ Subject
    print(f"\n📚 Subject: {Subject.objects.count()} รายการ")
    for subj in Subject.objects.all():
        print(f"   - {subj.name} (Active: {subj.is_active})")
    
    # ตรวจสอบ Book
    total_books = Book.objects.count()
    active_books = Book.objects.filter(is_active=True).count()
    available_books = Book.objects.filter(is_active=True, is_available=True).count()
    
    print(f"\n📖 Books:")
    print(f"   - ทั้งหมด: {total_books} เล่ม")
    print(f"   - Active: {active_books} เล่ม")
    print(f"   - Available: {available_books} เล่ม")
    
    # แสดงตัวอย่าง 5 เล่มแรก
    print(f"\n📋 ตัวอย่างหนังสือ 5 เล่มแรก:")
    books = Book.objects.filter(is_active=True, is_available=True).select_related('resource_type', 'subject')[:5]
    
    for i, book in enumerate(books, 1):
        print(f"   {i}. {book.title[:60]}")
        print(f"      Author: {book.author or 'N/A'}")
        print(f"      Type: {book.resource_type.name if book.resource_type else 'N/A'}")
        print(f"      Subject: {book.subject.name if book.subject else 'N/A'}")
        print(f"      Active: {book.is_active}, Available: {book.is_available}")
        print()
    
    # ตรวจสอบ Query ที่ใช้ใน View
    print("🔎 ทดสอบ Query จาก View:")
    view_books = Book.objects.filter(is_active=True, is_available=True).select_related('resource_type', 'subject')
    print(f"   Query ผลลัพธ์: {view_books.count()} เล่ม")
    
    if view_books.count() == 0:
        print("❌ ไม่มีหนังสือที่ตรงเงื่อนไข is_active=True, is_available=True")
        
        # ตรวจสอบ Field values
        all_books = Book.objects.all()
        print(f"\n🔍 ตรวจสอบค่า Boolean fields ใน {all_books.count()} หนังสือ:")
        
        active_true = all_books.filter(is_active=True).count()
        available_true = all_books.filter(is_available=True).count()
        
        print(f"   is_active=True: {active_true}")
        print(f"   is_available=True: {available_true}")
        print(f"   ทั้งคู่เป็น True: {all_books.filter(is_active=True, is_available=True).count()}")
        
        # แสดงตัวอย่าง field values
        print(f"\n📋 ตัวอย่างค่า Boolean fields (5 เล่มแรก):")
        for book in all_books[:5]:
            print(f"   - {book.title[:40]}: active={book.is_active}, available={book.is_available}")


if __name__ == '__main__':
    check_data()