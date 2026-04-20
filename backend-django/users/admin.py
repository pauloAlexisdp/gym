from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, WhitelistedEmail


@admin.register(WhitelistedEmail)
class WhitelistedEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    actions = ['activate_users', 'deactivate_users']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Rol', {'fields': ('role',)}),
    )

    @admin.action(description='Activar usuarios seleccionados')
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Desactivar usuarios seleccionados')
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
