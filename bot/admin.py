from django.contrib import admin

from bot.models import UserBotSettings, TimeInterval, SessionHistory, BotSession, TerminationApplication, BankRecord


def make_users_active(model_admin, request, queryset):
    queryset.update(is_active=True)


def make_users_inactive(model_admin, request, queryset):
    queryset.update(is_active=False)


make_users_active.short_description = 'Make selected active'
make_users_inactive.short_description = 'Make selected inactive'


@admin.register(UserBotSettings)
class UserBotSettingsAdmin(admin.ModelAdmin):
    base_model = UserBotSettings
    fieldsets = [
        ('General', {
            'fields': [
                ('user', 'is_active'),
                'points',
            ]
        }),
        ('Settings', {
            'fields': [
                'self_check_mode'
            ]
        }),
        ('Time intervals', {
            'fields': [
                ('study_plan_hours', 'study_plan_days_duration_time_interval'),
                'time_interval_auto_renewal',
            ]
        })
    ]
    actions = [make_users_active, make_users_inactive]
    save_on_top = True
    list_display = ['user', 'points', 'is_active']
    list_filter = ['is_active', 'self_check_mode']
    search_fields = ['user']


@admin.display
def assigned_user(obj):
    return str(obj.user_bot_settings.user)


@admin.register(TimeInterval)
class TimeIntervalAdmin(admin.ModelAdmin):
    base_model = TimeInterval
    fieldsets = [
        ('General', {
            'fields': [
                'user_bot_settings',
                'status'
            ]
        }),
        ('Duration', {
            'fields': [
                'start_time',
                'end_time',
            ]
        }),
        ('Plan', {
            'fields': [
                ('initial_duration', 'hours_target'),
            ]
        }),
        ('Result', {
            'fields': [
                ('hours_completed', 'penalty')
            ]
        })
    ]
    save_on_top = True
    list_display = [assigned_user, 'status', 'penalty']
    list_filter = ['status', 'start_time', 'end_time']
    search_fields = ['start_time', 'end_time']


@admin.register(SessionHistory)
class SessionHistoryAdmin(admin.ModelAdmin):
    base_model = SessionHistory
    fieldsets = [
        ('General', {
            'fields': [
                'user_bot_settings',
                'ending_cause'
            ]
        }),
        ('Duration', {
            'fields': [
                'start_time',
                'end_time',
            ]
        })
    ]
    save_on_top = True
    list_display = [assigned_user, 'ending_cause']
    list_filter = ['ending_cause', 'start_time', 'end_time']
    search_fields = ['start_time', 'end_time']


@admin.register(BotSession)
class BotSessionAdmin(admin.ModelAdmin):
    base_model = BotSession
    fieldsets = [
        ('General', {
            'fields': [
                'user_bot_settings',
                'start_time',
            ]
        }),
        ('Checks', {
            'fields': [
                'self_check_mode',
                'next_check_time',
            ]
        })
    ]
    save_on_top = True
    list_display = [assigned_user, 'start_time', 'next_check_time']
    list_filter = ['start_time']
    search_fields = ['start_time']


def accept_refund(model_admin, request, queryset):
    for interval in queryset:
        interval.accept_refund('Заявка одобрена')


def decline_refund(model_admin, request, queryset):
    for interval in queryset:
        interval.decline_refund('Заявка отклонена')


make_users_active.short_description = 'Accept selected refund'
make_users_inactive.short_description = 'Decline selected refund'


@admin.display
def assigned_user_interval(obj):
    return str(obj.time_interval.user_bot_settings.user)


@admin.register(TerminationApplication)
class TerminationApplicationAdmin(admin.ModelAdmin):
    base_model = TerminationApplication
    fieldsets = [
        ('General', {
            'fields': [
                'time_interval',
            ]
        }),
        ('Application', {
            'fields': [
                'message',
            ]
        }),
        ('Reply', {
            'fields': [
                'status',
                'reply',
            ]
        })
    ]
    actions = [accept_refund, decline_refund]
    save_on_top = True
    list_display = [assigned_user_interval, 'status']
    list_filter = ['status']
    readonly_fields = ['message']


@admin.register(BankRecord)
class BankRecordAdmin(admin.ModelAdmin):
    base_model = BankRecord
    fieldsets = [
        ('General', {
            'fields': [
                'user_bot_settings',
                'time',
            ]
        }),
        ('Penalty', {
            'fields': [
                'value',
                'reason'
            ]
        }),
    ]
    save_on_top = True
    list_display = [assigned_user, 'value', 'reason']
    list_filter = ['time', 'reason']
    search_fields = ['time']
