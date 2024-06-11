from django.db import models

class Information(models.Model):
    CATEGORY_CHOICES = [
        ('กิจกรรม', 'กิจกรรม'),
        ('โครงการ', 'โครงการ'),
        ('อบรม/สัมนา', 'อบรม/สัมนา'),
    ]

    title = models.CharField(max_length=255, verbose_name="หัวข้อ")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="หมวด")
    target_group = models.CharField(max_length=255, verbose_name="กลุ่มเป้าหมาย")
    date = models.DateField(verbose_name="วันที่", blank=True, null=True)
    time = models.CharField(max_length=20, verbose_name="เวลา", blank=True, null=True)
    location = models.CharField(max_length=255, verbose_name="สถานที่", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่ลงข้อมูล")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไขข้อมูล")
    subtitle = models.CharField(max_length=255, verbose_name="หัวข้อรอง", blank=True, null=True)
    description1 = models.TextField(verbose_name="คำอธิบายรูปภาพ", blank=True, null=True)
    
    # รูปภาพ 10 รูป
    image1 = models.ImageField(upload_to='imageBlogs/', verbose_name="รูปภาพ 1", blank=True, null=True)
    image2 = models.ImageField(upload_to='imageBlogs/', verbose_name="รูปภาพ 2", blank=True, null=True)
    image3 = models.ImageField(upload_to='imageBlogs/', verbose_name="รูปภาพ 3", blank=True, null=True)
    image4 = models.ImageField(upload_to='imageBlogs/', verbose_name="รูปภาพ 4", blank=True, null=True)
    image5 = models.ImageField(upload_to='imageBlogs/', verbose_name="รูปภาพ 5", blank=True, null=True)
    image6 = models.ImageField(upload_to='imageBlogs/', verbose_name="รูปภาพ 6", blank=True, null=True)
   
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ข้อมูล"
        verbose_name_plural = "ข้อมูลทั้งหมด"
