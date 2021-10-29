from django.contrib import admin

from main.models import User


def make_users_active(model_admin, request, queryset):
    queryset.update(is_active=True)


def make_users_inactive(model_admin, request, queryset):
    queryset.update(is_active=False)


make_users_active.short_description = 'Make selected active'
make_users_inactive.short_description = 'Make selected inactive'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    base_model = User
    fieldsets = [
        ('General', {
            'fields': [
                ('username', 'is_active'),
                ('first_name', 'last_name'),
                'email',
            ]
        }),
        ('Permissions', {
            'fields': [
                ('is_staff', 'is_superuser'),
                'groups',
                'user_permissions'
            ]
        }),
        ('Timings', {
            'fields': [
                'last_login',
                'date_joined'
            ]
        })
    ]
    actions = [make_users_active, make_users_inactive]
    save_on_top = True
    list_display = ['username', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    filter_horizontal = ['groups', 'user_permissions']
    readonly_fields = ['date_joined']
