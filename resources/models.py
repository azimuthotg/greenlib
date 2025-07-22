from django.db import models
from django.urls import reverse


class ResourceType(models.Model):
    """ประเภททรัพยากร เช่น E-book, หนังสือ, วารสาร"""
    
    name = models.CharField(max_length=100, verbose_name="ประเภท")
    description = models.TextField(blank=True, null=True, verbose_name="คำอธิบาย")
    is_active = models.BooleanField(default=True, verbose_name="ใช้งาน")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "ประเภททรัพยากร"
        verbose_name_plural = "ประเภททรัพยากร"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Subject(models.Model):
    """หมวดหมู่เรื่อง เช่น สิ่งแวดล้อม, ทรัพยากรน้ำ"""
    
    name = models.CharField(max_length=200, verbose_name="หมวดเรื่อง")
    dewey_range = models.CharField(max_length=50, blank=True, null=True, 
                                 verbose_name="ช่วงเลขหมู่ดิวอี้")
    description = models.TextField(blank=True, null=True, verbose_name="คำอธิบาย")
    is_active = models.BooleanField(default=True, verbose_name="ใช้งาน")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "หมวดเรื่อง"
        verbose_name_plural = "หมวดเรื่อง"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """ข้อมูลหนังสือ/ทรัพยากรสารสนเทศ"""
    
    # ข้อมูลพื้นฐาน
    title = models.TextField(verbose_name="ชื่อเรื่อง")
    author = models.CharField(max_length=500, blank=True, null=True, verbose_name="ผู้แต่ง")
    publisher = models.CharField(max_length=300, blank=True, null=True, verbose_name="สำนักพิมพ์")
    publication_year = models.PositiveIntegerField(blank=True, null=True, verbose_name="ปีที่พิมพ์")
    
    # การจำแนก
    call_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="เลขหมู่")
    isbn = models.CharField(max_length=17, blank=True, null=True, verbose_name="ISBN")
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE, verbose_name="ประเภท")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="หมวดเรื่อง")
    
    # ข้อมูลเพิ่มเติม
    description = models.TextField(blank=True, null=True, verbose_name="คำอธิบาย")
    pages = models.PositiveIntegerField(blank=True, null=True, verbose_name="จำนวนหน้า")
    language = models.CharField(max_length=50, default="ไทย", verbose_name="ภาษา")
    
    # ลิงก์ภายนอก
    opac_url = models.URLField(blank=True, null=True, verbose_name="ลิงก์ OPAC")
    external_url = models.URLField(blank=True, null=True, verbose_name="ลิงก์ภายนอก")
    
    # ข้อมูลระบบ
    order_number = models.PositiveIntegerField(blank=True, null=True, verbose_name="ลำดับ")
    is_featured = models.BooleanField(default=False, verbose_name="แนะนำ")
    is_available = models.BooleanField(default=True, verbose_name="มีให้บริการ")
    is_active = models.BooleanField(default=True, verbose_name="ใช้งาน")
    
    # วันที่
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่เพิ่ม")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไข")
    
    class Meta:
        verbose_name = "หนังสือ/ทรัพยากร"
        verbose_name_plural = "หนังสือ/ทรัพยากร"
        ordering = ['order_number', 'title']
        indexes = [
            models.Index(fields=['resource_type']),
            models.Index(fields=['subject']),
            models.Index(fields=['call_number']),
            models.Index(fields=['is_active', 'is_available']),
        ]
    
    def __str__(self):
        return self.title[:100] + ('...' if len(self.title) > 100 else '')
    
    def get_absolute_url(self):
        return reverse('resources:detail', kwargs={'pk': self.pk})
    
    @property
    def short_title(self):
        """ชื่อเรื่องย่อสำหรับแสดงในรายการ"""
        return self.title[:80] + ('...' if len(self.title) > 80 else '')
    
    @property
    def publication_info(self):
        """ข้อมูลการพิมพ์"""
        info = []
        if self.publisher:
            info.append(self.publisher)
        if self.publication_year:
            info.append(str(self.publication_year))
        return ', '.join(info) if info else None
    
    @property
    def has_external_link(self):
        """มีลิงก์ภายนอกหรือไม่"""
        return bool(self.opac_url or self.external_url)
    
    @property 
    def primary_link(self):
        """ลิงก์หลักที่ใช้"""
        return self.opac_url or self.external_url