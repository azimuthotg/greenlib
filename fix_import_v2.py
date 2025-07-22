#!/usr/bin/env python
"""
สคริปต์แก้ไข Import ให้ถูกต้อง - เวอร์ชั่น 2
- ชื่อหนังสือครบ
- ประเภทถูกต้อง (หนังสือ/E-book)
- เพิ่ม OPAC link
รัน: python fix_import_v2.py
"""

import os
import django
import pandas as pd

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webproject.settings')
django.setup()

from resources.models import Book, ResourceType, Subject

def fix_and_reimport():
    """ลบข้อมูลเก่าและ import ใหม่ให้ถูกต้อง"""
    
    # ลบข้อมูลเก่า
    print("🗑️ ลบข้อมูลเก่า...")
    deleted_count = Book.objects.all().delete()[0]
    print(f"✅ ลบแล้ว {deleted_count} รายการ")
    
    # อ่านไฟล์ Excel
    excel_file = 'capture/namebook.xlsx'
    if not os.path.exists(excel_file):
        print(f"❌ ไม่พบไฟล์ {excel_file}")
        return
    
    print(f"📖 อ่านไฟล์ {excel_file}...")
    df = pd.read_excel(excel_file)
    
    print(f"📊 Columns: {list(df.columns)}")
    print(f"📊 จำนวนแถว: {len(df)}")
    
    # ตรวจสอบว่ามี columns ที่ต้องการ
    if len(df.columns) < 4:
        print("❌ Excel ไม่มี columns เพียงพอ")
        return
    
    # กำหนด columns ตาม Excel structure
    title_col = df.columns[1]     # Column B = ชื่อหนังสือ
    author_col = df.columns[2]    # Column C = ผู้แต่ง  
    type_col = df.columns[3]      # Column D = ประเภท
    opac_col = df.columns[4] if len(df.columns) > 4 else None  # Column E = OPAC
    
    print(f"📝 Column Mapping:")
    print(f"   ชื่อหนังสือ: {title_col}")
    print(f"   ผู้แต่ง: {author_col}")
    print(f"   ประเภท: {type_col}")
    print(f"   OPAC: {opac_col}")
    
    # ดึง ResourceTypes
    resource_types = {}
    for rt in ResourceType.objects.all():
        resource_types[rt.name] = rt
    
    default_subject = Subject.objects.filter(name='สิ่งแวดล้อมทั่วไป').first()
    
    print(f"📚 ResourceTypes ที่มี: {list(resource_types.keys())}")
    
    # เริ่ม Import
    print("\n🚀 เริ่ม Import...")
    created_count = 0
    error_count = 0
    
    for index, row in df.iterrows():
        try:
            # ดึงชื่อหนังสือ
            title = str(row[title_col]).strip() if pd.notna(row[title_col]) else None
            if not title or len(title) < 3:
                error_count += 1
                continue
            
            # ดึงผู้แต่ง
            author = str(row[author_col]).strip() if pd.notna(row[author_col]) else None
            if author == '-':
                author = None
            
            # ดึงประเภท
            resource_type_name = str(row[type_col]).strip() if pd.notna(row[type_col]) else 'หนังสือ'
            
            # หา ResourceType ที่ตรงกัน
            resource_type = resource_types.get(resource_type_name)
            if not resource_type:
                # ถ้าไม่เจอ ใช้ default
                resource_type = resource_types.get('หนังสือ') or list(resource_types.values())[0]
            
            # ดึง OPAC URL
            opac_url = None
            if opac_col and pd.notna(row[opac_col]):
                opac_url = str(row[opac_col]).strip()
                if not opac_url.startswith('http'):
                    opac_url = None
            
            # ตรวจสอบซ้ำ
            if Book.objects.filter(title=title).exists():
                continue
            
            # สร้างหนังสือ
            book = Book.objects.create(
                title=title,
                author=author,
                resource_type=resource_type,
                subject=default_subject,
                opac_url=opac_url,
                language='ไทย',
                order_number=index + 1,
                is_active=True,
                is_available=True
            )
            
            created_count += 1
            
            # แสดงความคืบหน้า
            if created_count <= 10:
                print(f"✅ {created_count:3d}: [{resource_type.name}] {title[:50]}")
            elif created_count % 20 == 0:
                print(f"✅ {created_count:3d}: [{resource_type.name}] {title[:50]}")
                
        except Exception as e:
            error_count += 1
            print(f"❌ Error row {index+1}: {str(e)}")
    
    # สรุปผล
    print(f"\n🎉 Import เสร็จสิ้น!")
    print(f"   ✅ สร้างใหม่: {created_count} รายการ")
    print(f"   ❌ Error: {error_count} รายการ")
    
    # แสดงสถิติประเภท
    print(f"\n📊 สถิติตามประเภท:")
    for rt in ResourceType.objects.all():
        count = Book.objects.filter(resource_type=rt).count()
        if count > 0:
            print(f"   {rt.name}: {count} เล่ม")
    
    print(f"\n📚 รวมในระบบ: {Book.objects.count()} เล่ม")


if __name__ == '__main__':
    print("🔧 แก้ไขการ Import - รอบ 2...")
    print("="*50)
    fix_and_reimport()