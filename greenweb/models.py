from django.db import models
from category.models import Category

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    category_metric = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    attachment = models.FileField(upload_to='attachments/',blank=True)
    attachment_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category_metric} - {self.description[:50]}"
    
# Path: greenweb/models.py from chatgpt
class Year(models.Model):
    year = models.IntegerField(primary_key=True, verbose_name="ปี")

    def __str__(self):
        return str(self.year)

class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name="ชื่อหมวดหมู่")
    category_description = models.CharField(max_length=255, blank=True, null=True, verbose_name="คำอธิบายหมวดหมู่")
    year = models.ForeignKey(Year, on_delete=models.CASCADE, verbose_name="ปี", related_name="categories", default=2024)

    def __str__(self):
        return self.category_name

#class Category(models.Model):
#    category_name = models.CharField(max_length=255, verbose_name="ชื่อหมวดหมู่")
#    category_description = models.CharField(max_length=255, blank=True, null=True, verbose_name="คำอธิบายหมวดหมู่")

    def __str__(self):
        return self.category_name

class Issue(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='issues', verbose_name="หมวดหมู่")
    issue_name = models.CharField(max_length=255, verbose_name="ชื่อประเด็น")
    issue_description = models.TextField(blank=True, null=True, verbose_name="คำอธิบายประเด็น")

    def __str__(self):
        return self.issue_name

class Indicator(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='indicators', verbose_name="ประเด็น")
    indicator_name = models.CharField(max_length=255, verbose_name="ชื่อตัวชี้วัด")
    indicator_description = models.TextField(blank=True, null=True, verbose_name="คำอธิบายตัวชี้วัด")

    def __str__(self):
        return self.indicator_name

class Evidence(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='evidences', verbose_name="ตัวชี้วัด")
    evidence_name = models.CharField(max_length=255, verbose_name="ชื่อหลักฐาน")
    evidence_description = models.CharField(max_length=255, blank=True, null=True, verbose_name="คำอธิบายหลักฐาน")
    #evidence_file = models.CharField(max_length=255, blank=True, null=True, verbose_name="ไฟล์หลักฐาน")
    evidence_file = models.FileField(upload_to='evidences/2024/', blank=True, null=True)

    def __str__(self):
        return self.evidence_name
