# Generated by Django 5.0.4 on 2024-05-24 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='หัวข้อ')),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True, verbose_name='หัวข้อรอง')),
                ('category', models.CharField(choices=[('กิจกรรม', 'กิจกรรม'), ('โครงการ', 'โครงการ'), ('อบรม/สัมนา', 'อบรม/สัมนา')], max_length=50, verbose_name='หมวด')),
                ('target_group', models.CharField(max_length=255, verbose_name='กลุ่มเป้าหมาย')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='เวลา')),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='สถานที่')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='วันที่ลงข้อมูล')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='imageBlogs/', verbose_name='รูปภาพ 1')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='imageBlogs/', verbose_name='รูปภาพ 2')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='imageBlogs/', verbose_name='รูปภาพ 3')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='imageBlogs/', verbose_name='รูปภาพ 4')),
                ('image5', models.ImageField(blank=True, null=True, upload_to='imageBlogs/', verbose_name='รูปภาพ 5')),
                ('image6', models.ImageField(blank=True, null=True, upload_to='imageBlogs/', verbose_name='รูปภาพ 6')),
                ('image7', models.ImageField(blank=True, null=True, upload_to='imageBlogs/', verbose_name='รูปภาพ 7')),
                ('image8', models.ImageField(blank=True, null=True, upload_to='imageBlogs/', verbose_name='รูปภาพ 8')),
                ('image9', models.ImageField(blank=True, null=True, upload_to='imageBlogs/', verbose_name='รูปภาพ 9')),
                ('image10', models.ImageField(blank=True, null=True, upload_to='imageBlogs/', verbose_name='รูปภาพ 10')),
            ],
            options={
                'verbose_name': 'ข้อมูล',
                'verbose_name_plural': 'ข้อมูลทั้งหมด',
            },
        ),
    ]