import os
from django.db import models
from django.forms import Textarea
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.text import slugify
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Year(models.Model):
    year_id = models.AutoField(primary_key=True)
    year_name = models.CharField(max_length=255)
    year_description = models.TextField()

    def __str__(self):
        return str(self.year_name)

class CategoryGroup(models.Model):
    category_group_id = models.AutoField(primary_key=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='category_groups')
    group_name = models.CharField(max_length=255)
    group_description = models.TextField()

    def __str__(self):
        return str(self.group_name + ' (' + self.year.year_name + ')')

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_group = models.ForeignKey(CategoryGroup, on_delete=models.CASCADE, related_name='categories')
    category_name = models.CharField(max_length=255)
    category_description = models.TextField()

    def __str__(self):
        return str(self.category_name + ' (' + self.category_group.group_name + ')')

class Issue(models.Model):
    issue_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='issues')
    issue_name = models.CharField(max_length=255)
    issue_description = models.TextField()

    def __str__(self):
        return str(self.issue_name + ' (' + self.category.category_name + ')'+ ' (' + self.category.category_group.group_name + ')')

class Indicator(models.Model):
    indicator_id = models.AutoField(primary_key=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='indicators')
    indicator_name = models.CharField(max_length=255)
    indicator_description = models.TextField()
    
    def __str__(self):
        return str(self.indicator_name + ' (' + self.issue.issue_name + ')'+ ' (' + self.issue.category.category_name + ')'+ ' (' + self.issue.category.category_group.group_name + ')')

class Evidence(models.Model):
    evidence_id = models.AutoField(primary_key=True)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='evidences')
    evidence_name = models.CharField(max_length=255)
    evidence_description = models.TextField()
    evidence_file = models.FileField(upload_to='evidence/')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ผู้บันทึกข้อมูล")
    created_at = models.DateTimeField(default=now, verbose_name="วันที่บันทึกข้อมูล")

    def __str__(self):
        return str(self.evidence_name)
    
    def save(self, *args, **kwargs):
        if self.evidence_file:
            original_filename = self.evidence_file.name
            extension = os.path.splitext(original_filename)[1]
            new_filename = slugify(self.evidence_name) + extension
            self.evidence_file.name = os.path.join('evidence', new_filename)
        
        super().save(*args, **kwargs)

@receiver(post_delete, sender=Evidence)
def delete_evidence_file(sender, instance, **kwargs):
    if instance.evidence_file:
        if os.path.isfile(instance.evidence_file.path):
            os.remove(instance.evidence_file.path)
