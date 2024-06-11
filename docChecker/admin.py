from django.contrib import admin

# Register your models here.
from docChecker.models import Category, Issue, Indicator, Evidence, Year, CategoryGroup  # Import the CategoryGroup model

class YearAdmin(admin.ModelAdmin):
    list_display = ('year_name', 'year_description')
    ordering = ['year_id']  # การเรียงลำดับตามชื่อหมวดหมู่

class CategoryGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'group_description', 'year')
    ordering = ['category_group_id']  # การเรียงลำดับตามชื่อหมวดหมู่

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_description', 'category_group')
    ordering = ['category_group','category_id']  # การเรียงลำดับตามชื่อหมวดหมู่

class IssueAdmin(admin.ModelAdmin):
    list_display = ('issue_name', 'issue_description', 'category')
    ordering = ['issue_id']

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('indicator_name', 'indicator_description_short', 'issue')
    ordering = ['indicator_id']

    def indicator_description_short(self, obj):
        return obj.indicator_description[:100]

    indicator_description_short.short_description = 'Description (100ตัวอักษร)'

class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('evidence_name', 'evidence_description_short', 'indicator')
    ordering = ['indicator']

    def evidence_description_short(self, obj):
        return obj.evidence_description[:100]
    
    evidence_description_short.short_description = 'Description (100ตัวอักษร)'
    


admin.site.register(Year,YearAdmin)
admin.site.register(CategoryGroup,CategoryGroupAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Issue,IssueAdmin)
admin.site.register(Indicator,IndicatorAdmin)
admin.site.register(Evidence,EvidenceAdmin)