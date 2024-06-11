from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100,verbose_name="หมวดหมู่")
    category_issue = models.CharField(max_length=255,verbose_name="ประเด็น")
    category_metric = models.CharField(max_length=100,verbose_name="ตัวชี้วัด")
    category_description = models.TextField(verbose_name="อธิบาย", blank=True, null=True)
    categort_person = models.TextField(verbose_name="ผู้รับผิดชอบ", blank=True, null=True)


    def __str__(self):
        return f"{self.category_metric} - {self.category_description[:50] if self.category_description[:50] else ''}"