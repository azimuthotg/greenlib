#!/usr/bin/env python
"""
สคริปต์แก้ไขข้อมูลที่ import ผิด และ import ใหม่
รัน: python fix_import.py
"""

import os
import django
import pandas as pd

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webproject.settings')
django.setup()

from resources.models import Book, ResourceType, Subject

def fix_import():
    """ลบข้อมูลเก่าและ import ใหม่"""
    
    # ลบข้อมูลเก่า
    print("🗑️ ลบข้อมูลหนังสือเก่า...")
    deleted_count = Book.objects.all().delete()[0]
    print(f"✅ ลบแล้ว {deleted_count} รายการ")
    
    # อ่านไฟล์ Excel อีกครั้ง
    excel_file = 'capture/namebook.xlsx'
    if not os.path.exists(excel_file):
        print(f"❌ ไม่พบไฟล์ {excel_file}")
        return
    
    print(f"📖 อ่านไฟล์ {excel_file} ใหม่...")
    df = pd.read_excel(excel_file)
    
    print(f"📊 Columns: {list(df.columns)}")
    print("\n📋 ข้อมูล 5 แถวแรก:")
    for i in range(min(5, len(df))):
        print(f"--- แถวที่ {i+1} ---")
        for col in df.columns:
            value = df.iloc[i][col]
            if pd.notna(value):
                print(f"  {col}: {str(value)[:80]}")
        print()
    
    # จากรูป Excel เห็นว่า Column B คือชื่อหนังสือจริง
    print("✅ ใช้ Column ที่ 2 (index 1) เป็นชื่อหนังสือ")
    
    if len(df.columns) >= 2:
        title_col = df.columns[1]  # Column B (index 1)
    else:
        title_col = df.columns[0]  # fallback
    
    print(f"📝 Column ที่เลือก: '{title_col}'")
    
    # ตรวจสอบตัวอย่างข้อมูลจาก column ที่เลือก
    print(f"\n📋 ตัวอย่างชื่อหนังสือจาก '{title_col}':")
    sample_titles = df[title_col].dropna().head(10)
    for i, title in enumerate(sample_titles, 1):
        print(f"   {i:2d}. {str(title)[:80]}")
    
    print(f"\n✅ จะ import ด้วย column '{title_col}'...")
    
    return title_col, df


def import_with_correct_column(title_col, df):
    """Import ด้วย column ที่ถูกต้อง"""
    
    # ดึง ResourceType และ Subject เริ่มต้น
    default_type = ResourceType.objects.filter(name='หนังสือ').first()
    default_subject = Subject.objects.filter(name='สิ่งแวดล้อมทั่วไป').first()
    
    print(f"🚀 เริ่ม import ด้วย column '{title_col}'...")
    created_count = 0
    error_count = 0
    
    for index, row in df.iterrows():
        try:
            title = str(row[title_col]).strip() if pd.notna(row[title_col]) else None
            
            if not title or len(title) < 3:  # ชื่อหนังสือต้องยาวกว่า 3 ตัวอักษร
                error_count += 1
                continue
            
            # หา author จาก column อื่น
            author = None
            author_candidates = ['Author', 'ผู้แต่ง', 'author', 'นักเขียน']
            for col in author_candidates:
                if col in df.columns and pd.notna(row[col]):
                    author = str(row[col]).strip()
                    break
            
            # ตรวจสอบว่ามีหนังสือนี้แล้วหรือไม่
            if Book.objects.filter(title=title).exists():
                continue
            
            # สร้างหนังสือใหม่
            book = Book.objects.create(
                title=title,
                author=author,
                resource_type=default_type,
                subject=default_subject,
                language='ไทย',
                order_number=index + 1,
                is_active=True,
                is_available=True
            )
            
            created_count += 1
            if created_count <= 10:  # แสดงแค่ 10 รายการแรก
                print(f"✅ {created_count:3d}: {title[:60]}")
            elif created_count % 20 == 0:  # แสดงทุก 20 รายการ
                print(f"✅ {created_count:3d}: {title[:60]}")
                
        except Exception as e:
            error_count += 1
            print(f"❌ Error row {index+1}: {str(e)}")
    
    print(f"\n🎉 Import เสร็จสิ้น!")
    print(f"   ✅ สร้างใหม่: {created_count} รายการ")
    print(f"   ❌ Error: {error_count} รายการ")
    print(f"   📚 รวมในระบบ: {Book.objects.count()} เล่ม")


if __name__ == '__main__':
    print("🔧 แก้ไขข้อมูล Import...")
    print("="*50)
    
    title_col, df = fix_import()
    
    # Import ทันที (ไม่ต้องรอ input)
    import_with_correct_column(title_col, df)