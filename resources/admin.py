from django.contrib import admin
from django.utils.html import format_html
from .models import ResourceType, Subject, Book


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'dewey_range', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'dewey_range', 'description')
    ordering = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'short_title_display',
        'author',
        'resource_type',
        'call_number',
        'publication_year',
        'external_links',
        'is_featured',
        'is_available'
    )
    
    list_filter = (
        'resource_type',
        'subject',
        'is_featured',
        'is_available',
        'is_active',
        'publication_year',
        'language',
        'created_at'
    )
    
    search_fields = (
        'title',
        'author',
        'publisher',
        'call_number',
        'isbn',
        'description'
    )
    
    ordering = ('order_number', 'title')
    
    fieldsets = (
        ('ข้อมูลพื้นฐาน', {
            'fields': (
                'title',
                'author',
                'publisher',
                'publication_year',
                'language',
                'pages'
            )
        }),
        
        ('การจำแนก', {
            'fields': (
                'resource_type',
                'subject',
                'call_number',
                'isbn'
            )
        }),
        
        ('รายละเอียด', {
            'fields': (
                'description',
                'opac_url',
                'external_url'
            )
        }),
        
        ('การจัดการ', {
            'fields': (
                'order_number',
                'is_featured',
                'is_available',
                'is_active'
            )
        })
    )
    
    def short_title_display(self, obj):
        """แสดงชื่อเรื่องย่อ"""
        return obj.short_title
    short_title_display.short_description = 'ชื่อเรื่อง'
    
    def external_links(self, obj):
        """แสดงลิงก์ภายนอก"""
        links = []
        
        if obj.opac_url:
            links.append(f'<a href="{obj.opac_url}" target="_blank" title="ดู OPAC">📚 OPAC</a>')
            
        if obj.external_url:
            links.append(f'<a href="{obj.external_url}" target="_blank" title="ลิงก์ภายนอก">🔗 Link</a>')
        
        return format_html(' | '.join(links)) if links else '-'
    external_links.short_description = 'ลิงก์'
    
    # Actions
    actions = ['mark_as_featured', 'mark_as_not_featured', 'mark_as_available', 'mark_as_unavailable']
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'ตั้งเป็นแนะนำแล้ว {updated} รายการ')
    mark_as_featured.short_description = 'ตั้งเป็นรายการแนะนำ'
    
    def mark_as_not_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'ยกเลิกการแนะนำแล้ว {updated} รายการ')
    mark_as_not_featured.short_description = 'ยกเลิกการแนะนำ'
    
    def mark_as_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'ตั้งเป็นพร้อมให้บริการแล้ว {updated} รายการ')
    mark_as_available.short_description = 'ตั้งเป็นพร้อมให้บริการ'
    
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'ตั้งเป็นไม่พร้อมให้บริการแล้ว {updated} รายการ')
    mark_as_unavailable.short_description = 'ตั้งเป็นไม่พร้อมให้บริการ'