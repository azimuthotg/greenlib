from django.contrib import admin
from django.utils.html import format_html
from .models import PromotionalCategory, PromotionalImage


@admin.register(PromotionalCategory)
class PromotionalCategoryAdmin(admin.ModelAdmin):
    list_display = ['name_th', 'name_en', 'total_images', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name_th', 'name_en', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('ข้อมูลหมวดหมู่', {
            'fields': ('name_th', 'name_en', 'description', 'is_active')
        }),
        ('ข้อมูลระบบ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class PromotionalImageInline(admin.TabularInline):
    model = PromotionalImage
    extra = 1
    fields = ['title', 'image', 'display_order', 'is_featured', 'is_active']
    readonly_fields = ['file_size_display']
    
    def file_size_display(self, obj):
        if obj.file_size_mb:
            return f"{obj.file_size_mb} MB"
        return "-"
    file_size_display.short_description = "ขนาดไฟล์"


@admin.register(PromotionalImage)
class PromotionalImageAdmin(admin.ModelAdmin):
    list_display = ['image_thumbnail', 'title', 'category', 'display_order', 'file_size_display', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'tags', 'category__name_th']
    readonly_fields = ['created_at', 'updated_at', 'file_size', 'image_preview']
    list_editable = ['display_order', 'is_featured', 'is_active']
    
    fieldsets = (
        ('ข้อมูลรูปภาพ', {
            'fields': ('category', 'title', 'description', 'image', 'image_preview', 'alt_text')
        }),
        ('การจัดการ', {
            'fields': ('tags', 'display_order', 'is_featured', 'is_active')
        }),
        ('ข้อมูลระบบ', {
            'fields': ('created_at', 'updated_at', 'file_size'),
            'classes': ('collapse',)
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "ไม่มีรูปภาพ"
    image_thumbnail.short_description = "รูปภาพ"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain;" />',
                obj.image.url
            )
        return "ไม่มีรูปภาพ"
    image_preview.short_description = "ตัวอย่างรูปภาพ"
    
    def file_size_display(self, obj):
        if obj.file_size_mb:
            return f"{obj.file_size_mb} MB"
        return "-"
    file_size_display.short_description = "ขนาดไฟล์"


# เพิ่ม inline ให้ Category
PromotionalCategoryAdmin.inlines = [PromotionalImageInline]