from django.contrib import admin
from greenweb.models import Category,Issue,Indicator,Evidence,Year  # Import the Year model
# Register your models here.

# Register the Year model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_description', 'year')
    ordering = ['category_name']  # การเรียงลำดับตามชื่อหมวดหมู่

class IssueAdmin(admin.ModelAdmin):
    list_display = ('issue_name', 'issue_description', 'category')
    ordering = ['issue_name']

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('indicator_name', 'indicator_description', 'issue')
    ordering = ['indicator_name']

class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('evidence_name', 'evidence_description', 'indicator')
    ordering = ['evidence_name']


admin.site.register(Year)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Evidence, EvidenceAdmin)
