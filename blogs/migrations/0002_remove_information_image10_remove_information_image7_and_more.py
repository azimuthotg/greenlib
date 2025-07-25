# Generated by Django 5.0.4 on 2024-05-24 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='information',
            name='image10',
        ),
        migrations.RemoveField(
            model_name='information',
            name='image7',
        ),
        migrations.RemoveField(
            model_name='information',
            name='image8',
        ),
        migrations.RemoveField(
            model_name='information',
            name='image9',
        ),
        migrations.AddField(
            model_name='information',
            name='description1',
            field=models.TextField(blank=True, null=True, verbose_name='คำอธิบายรูปภาพ'),
        ),
        migrations.AddField(
            model_name='information',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='วันที่แก้ไขข้อมูล'),
        ),
    ]
