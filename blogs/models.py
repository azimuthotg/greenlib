import os
from django.db import models
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import pre_save

def image_upload_to(instance, filename):
    # Extract the extension of the file
    extension = filename.split('.')[-1]
    
    # Generate the base name using the date
    if instance.date:
        base_name = instance.date.strftime('%Y-%m-%d')
    else:
        base_name = now().strftime('%Y-%m-%d')
    
    # Find the field name of the current image being processed
    for field_name in ['image1', 'image2', 'image3', 'image4', 'image5', 'image6']:
        if getattr(instance, field_name).name == filename:
            # Get the count of images with the same date and suffix index
            model = instance.__class__
            count = model.objects.filter(date=instance.date).count()
            suffix = int(field_name.replace('image', ''))
            new_filename = f"{base_name}-{count}-{suffix}.{extension}"
            return os.path.join('imageBlogs/', new_filename)
    return os.path.join('imageBlogs/', filename)

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
    image1 = models.ImageField(upload_to=image_upload_to, verbose_name="รูปภาพ 1", blank=True, null=True)
    image2 = models.ImageField(upload_to=image_upload_to, verbose_name="รูปภาพ 2", blank=True, null=True)
    image3 = models.ImageField(upload_to=image_upload_to, verbose_name="รูปภาพ 3", blank=True, null=True)
    image4 = models.ImageField(upload_to=image_upload_to, verbose_name="รูปภาพ 4", blank=True, null=True)
    image5 = models.ImageField(upload_to=image_upload_to, verbose_name="รูปภาพ 5", blank=True, null=True)
    image6 = models.ImageField(upload_to=image_upload_to, verbose_name="รูปภาพ 6", blank=True, null=True)
   
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ข้อมูล"
        verbose_name_plural = "ข้อมูลทั้งหมด"

# Signal to update image name before saving
@receiver(pre_save, sender=Information)
def update_image_filename(sender, instance, **kwargs):
    for field_name in ['image1', 'image2', 'image3', 'image4', 'image5', 'image6']:
        image_field = getattr(instance, field_name)
        if image_field:
            image_field.name = image_upload_to(instance, image_field.name)
# Path: blogs/admin.py