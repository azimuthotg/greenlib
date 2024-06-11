from django.contrib import admin
from .models import Information

admin.site.register(Information)

class InformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'target_group', 'created_at')
    search_fields = ('title', 'category', 'target_group')
    list_filter = ('category', 'created_at')
    # เพิ่มฟิลด์รูปภาพในหน้าแอดมิน
    readonly_fields = ('image1', 'image2', 'image3', 'image4', 'image5', 'image6')