from django.contrib import admin
from .models import Activity, HomePageConfig, Schedule


@admin.register(HomePageConfig)
class HomePageConfigAdmin(admin.ModelAdmin):
    fields = (
        'hero_title', 'about_title', 'about_description', 'activities_title',
        'background_color', 'background_image',
        'map_embed_url', 'facebook_url', 'instagram_url', 'whatsapp_url',
    )

    def has_add_permission(self, request):
        return not HomePageConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order',)
