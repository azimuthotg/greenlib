from django.contrib import admin
from info_graph.models import Year, Month, DataEntry

# Register your models here.
admin.site.register(Year)
admin.site.register(Month)
admin.site.register(DataEntry)