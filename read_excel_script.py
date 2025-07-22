#!/usr/bin/env python
"""
Script สำหรับอ่านข้อมูลจาก Excel file
รัน: python read_excel_script.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webproject.settings')
django.setup()

def read_excel_data():
    try:
        import pandas as pd
        
        # อ่านไฟล์ Excel
        excel_file = 'capture/namebook.xlsx'
        print(f"กำลังอ่านไฟล์: {excel_file}")
        print("=" * 60)
        
        df = pd.read_excel(excel_file)
        
        # แสดงข้อมูลพื้นฐาน
        print(f"📊 จำนวนแถว: {len(df)}")
        print(f"📊 จำนวนคอลัมน์: {len(df.columns)}")
        print("📊 ชื่อคอลัมน์:", df.columns.tolist())
        print("=" * 60)
        
        # แสดงข้อมูล 5 แถวแรก
        print("📖 ข้อมูล 5 แถวแรก:")
        print("=" * 60)
        
        for i in range(min(5, len(df))):
            print(f"\n📚 แถวที่ {i+1}:")
            print("-" * 40)
            
            for col in df.columns:
                value = str(df.iloc[i][col])
                
                # จำกัดความยาวข้อความ
                if len(value) > 150:
                    value = value[:150] + "..."
                
                # แสดงผลสวยงาม
                print(f"  {col:15}: {value}")
        
        print("\n" + "=" * 60)
        print("✅ อ่านข้อมูลเสร็จสิ้น")
        
        # แสดงสถิติเพิ่มเติม
        print(f"\n📈 สถิติเพิ่มเติม:")
        print(f"  - แถวที่มีข้อมูลครบ: {df.dropna().shape[0]}")
        print(f"  - แถวที่มีข้อมูลหาย: {df.isnull().any(axis=1).sum()}")
        
        # ตรวจสอบคอลัมน์ที่สำคัญ
        important_cols = ['รายการ', 'เลขหมู่', 'ประเภท', 'OPAC']
        for col in important_cols:
            if col in df.columns:
                unique_count = df[col].nunique()
                print(f"  - {col}: {unique_count} ค่าที่แตกต่างกัน")
        
        return df
        
    except ImportError:
        print("❌ Error: ต้องติดตั้ง pandas และ openpyxl")
        print("รันคำสั่ง: pip install pandas openpyxl")
        return None
        
    except FileNotFoundError:
        print(f"❌ Error: ไม่พบไฟล์ {excel_file}")
        print("กรุณาตรวจสอบว่าไฟล์อยู่ใน folder capture/")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 เริ่มต้นอ่านข้อมูล Excel...")
    data = read_excel_data()
    
    if data is not None:
        print("\n📋 พร้อมสำหรับขั้นตอนถัดไป!")
    else:
        print("\n💥 มีปัญหาในการอ่านข้อมูล")