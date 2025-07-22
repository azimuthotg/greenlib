#!/usr/bin/env python
"""
สคริปต์สร้างข้อมูลเบื้องต้นสำหรับ Resources app
รัน: python setup_resources_data.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webproject.settings')
django.setup()

from resources.models import ResourceType, Subject

def create_resource_types():
    """สร้างประเภททรัพยากร"""
    types_data = [
        {'name': 'E-book', 'description': 'หนังสือดิจิทัล'},
        {'name': 'หนังสือ', 'description': 'หนังสือเล่มจริง'},
        {'name': 'วารสาร', 'description': 'วารสารวิชาการ'},
        {'name': 'รายงานการวิจัย', 'description': 'รายงานการวิจัย'},
        {'name': 'เอกสารอ้างอิง', 'description': 'เอกสารอ้างอิง'},
    ]
    
    created_count = 0
    for data in types_data:
        resource_type, created = ResourceType.objects.get_or_create(
            name=data['name'],
            defaults={
                'description': data['description'],
                'is_active': True
            }
        )
        if created:
            created_count += 1
            print(f"✅ สร้าง ResourceType: {resource_type.name}")
        else:
            print(f"ℹ️  มี ResourceType อยู่แล้ว: {resource_type.name}")
    
    print(f"📊 สร้าง ResourceType ใหม่ {created_count} รายการ")


def create_subjects():
    """สร้างหมวดเรื่อง"""
    subjects_data = [
        {'name': 'สิ่งแวดล้อมทั่วไป', 'description': 'หนังสือเกี่ยวกับสิ่งแวดล้อมทั่วไป'},
        {'name': 'การจัดการขยะ', 'description': 'การจัดการขยะและของเสีย'},
        {'name': 'พลังงานหมุนเวียน', 'description': 'พลังงานสะอาดและหมุนเวียน'},
        {'name': 'การเปลี่ยนแปลงสภาพภูมิอากาศ', 'description': 'สภาพภูมิอากาศและการปรับตัว'},
        {'name': 'การอนุรักษ์ธรรมชาติ', 'description': 'การอนุรักษ์และคุ้มครองธรรมชาติ'},
        {'name': 'เกษตรยั่งยืน', 'description': 'เกษตรกรรมที่เป็นมิตรต่อสิ่งแวดล้อม'},
        {'name': 'การพัฒนาที่ยั่งยืน', 'description': 'การพัฒนาอย่างยั่งยืน'},
        {'name': 'มลพิษสิ่งแวดล้อม', 'description': 'มลพิษทางอากาศ น้ำ และดิน'},
        {'name': 'ป่าไผ่และไม้ไผ่', 'description': 'การใช้ประโยชน์จากไผ่'},
        {'name': 'เทคโนโลยีสิ่งแวดล้อม', 'description': 'เทคโนโลยีเพื่อสิ่งแวดล้อม'},
    ]
    
    created_count = 0
    for data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            name=data['name'],
            defaults={
                'description': data['description'],
                'is_active': True
            }
        )
        if created:
            created_count += 1
            print(f"✅ สร้าง Subject: {subject.name}")
        else:
            print(f"ℹ️  มี Subject อยู่แล้ว: {subject.name}")
    
    print(f"📊 สร้าง Subject ใหม่ {created_count} รายการ")


if __name__ == '__main__':
    print("🚀 เริ่มสร้างข้อมูลเบื้องต้นสำหรับ Resources...")
    print("=" * 50)
    
    # สร้าง ResourceType
    print("\n📁 สร้าง ResourceType...")
    create_resource_types()
    
    # สร้าง Subject
    print("\n📚 สร้าง Subject...")
    create_subjects()
    
    print("\n" + "=" * 50)
    print("✨ เสร็จสิ้นการสร้างข้อมูลเบื้องต้น!")
    print("📋 สถิติ:")
    print(f"   ResourceType: {ResourceType.objects.count()} รายการ")
    print(f"   Subject: {Subject.objects.count()} รายการ")
    print(f"   Book: {0} รายการ (รอ import)")