from django.contrib import admin
from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_featured', 'is_active', 'order')
    list_editable = ('order', 'is_active', 'is_featured')
    ordering = ('order',)
