import os
from django.db import models
from django.utils.timezone import now


def promotional_image_upload_to(instance, filename):
    """
    สร้างเส้นทางสำหรับอัพโหลดรูปภาพสื่อประชาสัมพันธ์
    promotional/category_name/filename
    """
    extension = filename.split('.')[-1]
    category_name = instance.category.name_en if instance.category.name_en else 'general'
    # ทำให้ชื่อไฟล์ปลอดภัย
    safe_filename = f"{instance.id or 'new'}_{now().strftime('%Y%m%d_%H%M%S')}.{extension}"
    return os.path.join('promotional', category_name, safe_filename)


class PromotionalCategory(models.Model):
    """หมวดหมู่สื่อประชาสัมพันธ์"""
    
    name_th = models.CharField(max_length=200, verbose_name="ชื่อหมวดหมู่ (ไทย)")
    name_en = models.CharField(max_length=200, blank=True, null=True, verbose_name="ชื่อหมวดหมู่ (อังกฤษ)")
    description = models.TextField(blank=True, null=True, verbose_name="คำอธิบายหมวดหมู่")
    is_active = models.BooleanField(default=True, verbose_name="ใช้งาน")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไข")
    
    class Meta:
        verbose_name = "หมวดหมู่สื่อประชาสัมพันธ์"
        verbose_name_plural = "หมวดหมู่สื่อประชาสัมพันธ์"
        ordering = ['name_th']
    
    def __str__(self):
        return self.name_th
    
    @property
    def total_images(self):
        """จำนวนรูปภาพทั้งหมดในหมวดหมู่นี้"""
        return self.images.filter(is_active=True).count()


class PromotionalImage(models.Model):
    """รูปภาพสื่อประชาสัมพันธ์"""
    
    category = models.ForeignKey(
        PromotionalCategory, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="หมวดหมู่"
    )
    title = models.CharField(max_length=200, verbose_name="ชื่อรูปภาพ")
    description = models.TextField(blank=True, null=True, verbose_name="คำอธิบายรูปภาพ")
    image = models.ImageField(upload_to=promotional_image_upload_to, verbose_name="รูปภาพ")
    alt_text = models.CharField(max_length=200, blank=True, null=True, verbose_name="ข้อความทดแทน")
    
    # ข้อมูลเพิ่มเติม
    tags = models.CharField(max_length=500, blank=True, null=True, verbose_name="แท็ก (คั่นด้วยจุลภาค)")
    display_order = models.PositiveIntegerField(default=0, verbose_name="ลำดับการแสดง")
    is_featured = models.BooleanField(default=False, verbose_name="รูปภาพเด่น")
    is_active = models.BooleanField(default=True, verbose_name="ใช้งาน")
    
    # ข้อมูลระบบ
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่อัพโหลด")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไข")
    file_size = models.PositiveIntegerField(null=True, blank=True, verbose_name="ขนาดไฟล์ (ไบต์)")
    
    class Meta:
        verbose_name = "รูปภาพสื่อประชาสัมพันธ์"
        verbose_name_plural = "รูปภาพสื่อประชาสัมพันธ์"
        ordering = ['category', 'display_order', '-created_at']
    
    def __str__(self):
        return f"{self.category.name_th} - {self.title}"
    
    def save(self, *args, **kwargs):
        """บันทึกและคำนวณขนาดไฟล์"""
        super().save(*args, **kwargs)
        
        if self.image and not self.file_size:
            try:
                self.file_size = self.image.size
                super().save(update_fields=['file_size'])
            except:
                pass
    
    @property
    def file_size_mb(self):
        """ขนาดไฟล์ในหน่วย MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return None
    
    @property
    def tag_list(self):
        """แปลงแท็กเป็น list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []