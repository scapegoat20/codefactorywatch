from django.contrib import admin
from .models import Finding, Pillar, Technique

admin.site.register(Pillar)
admin.site.register(Technique)


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ("title", "technique", "severity", "status", "date_found")
    list_filter = ("severity", "status", "technique__pillar")
