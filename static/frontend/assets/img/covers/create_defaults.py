#!/usr/bin/env python3
"""
สคริปต์สร้างรูป default สำหรับประเภทสื่อต่างๆ
รันด้วย: python create_defaults.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ขนาดรูป
WIDTH = 120
HEIGHT = 160

# สีสำหรับแต่ละประเภท
COLORS = {
    'book': {'bg': '#4CAF50', 'text': '#FFFFFF'},      # เขียว - หนังสือ
    'ebook': {'bg': '#2196F3', 'text': '#FFFFFF'},     # น้ำเงิน - E-book
    'journal': {'bg': '#FF9800', 'text': '#FFFFFF'},   # ส้ม - วารสาร
    'research': {'bg': '#E91E63', 'text': '#FFFFFF'},  # ชมพู - รายงานวิจัย
    'reference': {'bg': '#9C27B0', 'text': '#FFFFFF'}, # ม่วง - เอกสารอ้างอิง
    'media': {'bg': '#607D8B', 'text': '#FFFFFF'}      # เทา - อื่นๆ
}

# ข้อความสำหรับแต่ละประเภท
TEXTS = {
    'book': ['หนังสือ', 'BOOK'],
    'ebook': ['E-book', 'DIGITAL'],
    'journal': ['วารสาร', 'JOURNAL'],
    'research': ['รายงาน', 'RESEARCH'], 
    'reference': ['อ้างอิง', 'REFERENCE'],
    'media': ['สื่อ', 'MEDIA']
}

def create_default_cover(type_name):
    """สร้างรูปปกสำหรับประเภทสื่อ"""
    
    # สร้างภาพพื้นฐาน
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS[type_name]['bg'])
    draw = ImageDraw.Draw(img)
    
    # วาดเฟรม
    frame_width = 3
    draw.rectangle([frame_width, frame_width, WIDTH-frame_width, HEIGHT-frame_width], 
                  outline='white', width=2)
    
    # เพิ่มไอคอน/สัญลักษณ์
    if type_name == 'book':
        # วาดรูปหนังสือ
        draw.rectangle([30, 40, 90, 120], fill='white', outline=COLORS[type_name]['bg'], width=2)
        draw.rectangle([35, 45, 85, 115], outline=COLORS[type_name]['bg'], width=1)
        
    elif type_name == 'ebook':
        # วาดรูปแท็บเล็ต
        draw.rectangle([25, 35, 95, 125], fill='white', outline='lightblue', width=2)
        draw.rectangle([30, 40, 90, 120], fill='lightblue')
        
    elif type_name == 'journal':
        # วาดรูปวารสาร
        for i in range(3):
            y = 50 + i * 15
            draw.rectangle([25, y, 95, y+10], fill='white', outline='orange', width=1)
            
    elif type_name == 'research':
        # วาดรูปรายงาน
        draw.rectangle([30, 40, 90, 120], fill='white', outline='pink', width=2)
        for i in range(6):
            y = 50 + i * 10
            draw.line([40, y, 80, y], fill=COLORS[type_name]['bg'], width=1)
            
    elif type_name == 'reference':
        # วาดรูปพจนานุกรม
        draw.rectangle([25, 35, 95, 125], fill='white', outline='purple', width=3)
        draw.rectangle([30, 40, 90, 50], fill=COLORS[type_name]['bg'])
        
    else:  # media
        # วาดรูปสื่อทั่วไป
        draw.ellipse([35, 50, 85, 100], fill='white', outline='gray', width=2)
        draw.ellipse([50, 65, 70, 85], fill=COLORS[type_name]['bg'])
    
    # เพิ่มข้อความ
    try:
        # ใช้ฟอนต์ default
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    except:
        font_large = None
        font_small = None
    
    # ข้อความภาษาไทย
    thai_text = TEXTS[type_name][0]
    eng_text = TEXTS[type_name][1]
    
    # คำนวณตำแหน่งข้อความ
    text_bbox = draw.textbbox((0, 0), thai_text, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (WIDTH - text_width) // 2
    
    # วาดข้อความภาษาไทย
    draw.text((text_x, HEIGHT - 35), thai_text, fill='white', font=font_large)
    
    # ข้อความอังกฤษ
    text_bbox = draw.textbbox((0, 0), eng_text, font=font_small)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (WIDTH - text_width) // 2
    draw.text((text_x, HEIGHT - 20), eng_text, fill='white', font=font_small)
    
    return img

def main():
    """สร้างรูป default ทั้งหมด"""
    
    # สร้างโฟลเดอร์ถ้ายังไม่มี
    os.makedirs('.', exist_ok=True)
    
    # สร้างรูปสำหรับแต่ละประเภท
    for type_name in COLORS.keys():
        filename = f'default-{type_name}.png'
        
        print(f'กำลังสร้าง {filename}...')
        img = create_default_cover(type_name)
        img.save(filename, 'PNG', quality=95)
        print(f'สร้าง {filename} เรียบร้อย')
    
    print('\nสร้างรูป default ทั้งหมดเรียบร้อยแล้ว!')
    print('ไฟล์ที่สร้าง:')
    for type_name in COLORS.keys():
        print(f'- default-{type_name}.png')

if __name__ == '__main__':
    main()