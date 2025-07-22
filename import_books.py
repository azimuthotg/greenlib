#!/usr/bin/env python
"""
สคริปต์ import ข้อมูลหนังสือ 199 เล่มจาก Excel
รัน: python import_books.py
"""

import os
import django
import pandas as pd
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webproject.settings')
django.setup()

from resources.models import Book, ResourceType, Subject

def import_books_from_excel():
    """Import หนังสือจากไฟล์ Excel"""
    
    excel_file = 'capture/namebook.xlsx'
    
    if not os.path.exists(excel_file):
        print(f"❌ ไม่พบไฟล์ {excel_file}")
        print("📝 กรุณาตรวจสอบว่าไฟล์อยู่ในโฟล์เดอร์ capture/")
        return
    
    try:
        # อ่านไฟล์ Excel
        print(f"📖 กำลังอ่านไฟล์ {excel_file}...")
        df = pd.read_excel(excel_file)
        
        print(f"📊 พบข้อมูล {len(df)} รายการ")
        print("📋 Columns:", list(df.columns))
        
        # แสดงตัวอย่างข้อมูล 3 แถวแรก
        print("\n📋 ตัวอย่างข้อมูล 3 แถวแรก:")
        for i in range(min(3, len(df))):
            print(f"--- แถวที่ {i+1} ---")
            for col in df.columns:
                value = df.iloc[i][col]
                if pd.notna(value):
                    print(f"  {col}: {str(value)[:100]}")
        
        # ดึง ResourceType เริ่มต้น (หนังสือ)
        default_type = ResourceType.objects.filter(name='หนังสือ').first()
        if not default_type:
            default_type = ResourceType.objects.first()
        
        # ดึง Subject เริ่มต้น (สิ่งแวดล้อมทั่วไป)
        default_subject = Subject.objects.filter(name='สิ่งแวดล้อมทั่วไป').first()
        if not default_subject:
            default_subject = Subject.objects.first()
        
        print(f"✅ ใช้ ResourceType เริ่มต้น: {default_type}")
        print(f"✅ ใช้ Subject เริ่มต้น: {default_subject}")
        
        # เริ่ม import
        print("\n🚀 เริ่มต้น import...")
        created_count = 0
        error_count = 0
        
        for index, row in df.iterrows():
            try:
                # หาคอลัมน์ที่มีข้อมูลชื่อหนังสือ (ลองหลายชื่อ)
                title_candidates = ['Title', 'ชื่อเรื่อง', 'title', 'ชื่อ', 'หนังสือ', 'Book']
                title = None
                
                for col in title_candidates:
                    if col in df.columns and pd.notna(row[col]) and str(row[col]).strip():
                        title = str(row[col]).strip()
                        break
                
                # ถ้าไม่เจอชื่อ ใช้คอลัมน์แรก
                if not title:
                    first_col = df.columns[0]
                    if pd.notna(row[first_col]):
                        title = str(row[first_col]).strip()
                
                if not title:
                    print(f"⚠️  แถวที่ {index+1}: ไม่มีชื่อหนังสือ")
                    error_count += 1
                    continue
                
                # หาคอลัมน์ผู้แต่ง
                author_candidates = ['Author', 'ผู้แต่ง', 'author', 'นักเขียน']
                author = None
                for col in author_candidates:
                    if col in df.columns and pd.notna(row[col]):
                        author = str(row[col]).strip()
                        break
                
                # หาคอลัมน์เลขหมู่
                call_number_candidates = ['Call Number', 'เลขหมู่', 'call_number', 'CallNumber']
                call_number = None
                for col in call_number_candidates:
                    if col in df.columns and pd.notna(row[col]):
                        call_number = str(row[col]).strip()
                        break
                
                # หาคอลัมน์สำนักพิมพ์
                publisher_candidates = ['Publisher', 'สำนักพิมพ์', 'publisher', 'ผู้พิมพ์']
                publisher = None
                for col in publisher_candidates:
                    if col in df.columns and pd.notna(row[col]):
                        publisher = str(row[col]).strip()
                        break
                
                # ตรวจสอบว่ามีหนังสือนี้อยู่แล้วหรือไม่
                existing_book = Book.objects.filter(title=title).first()
                if existing_book:
                    print(f"ℹ️  แถวที่ {index+1}: มีหนังสือนี้อยู่แล้ว - {title[:50]}")
                    continue
                
                # สร้างหนังสือใหม่
                book = Book.objects.create(
                    title=title,
                    author=author,
                    publisher=publisher,
                    call_number=call_number,
                    resource_type=default_type,
                    subject=default_subject,
                    language='ไทย',
                    order_number=index + 1,  # ใช้ลำดับจาก Excel
                    is_active=True,
                    is_available=True,
                    is_featured=False
                )
                
                created_count += 1
                print(f"✅ {created_count:3d}: {title[:60]}")
                
            except Exception as e:
                error_count += 1
                print(f"❌ แถวที่ {index+1}: Error - {str(e)}")
        
        # สรุปผล
        print("\n" + "="*60)
        print("🎉 เสร็จสิ้นการ import!")
        print(f"📊 สถิติ:")
        print(f"   ✅ สร้างใหม่: {created_count} รายการ")
        print(f"   ❌ Error: {error_count} รายการ")
        print(f"   📚 รวมหนังสือในระบบ: {Book.objects.count()} เล่ม")
        
    except FileNotFoundError:
        print(f"❌ ไม่พบไฟล์ {excel_file}")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {str(e)}")


if __name__ == '__main__':
    print("📚 เริ่ม import หนังสือจาก Excel...")
    print("="*60)
    import_books_from_excel()