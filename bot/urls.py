from django.urls import path, include

from bot import views as bot_views, ajax_views as bot_ajax_views

# url '/bot/ajax/...
bot_ajax_urls = [
    path('register/', bot_ajax_views.register_request, name='bot-ajax-register'),
    path('edit-settings/', bot_ajax_views.edit_settings_request, name='bot-ajax-edit_settings'),
    path('start-time-interval', bot_ajax_views.start_time_interval_request, name='bot-ajax-start_time_interval'),
    path('start-bot-session', bot_ajax_views.start_bot_session_request, name='bot-ajax-start_bot_session'),
    path('premature-termination/', bot_ajax_views.premature_termination_request, name='bot-ajax-premature_termination'),
    path('submit-check/', bot_ajax_views.submit_check_request, name='bot-ajax-submit_check'),
    path('check-update/', bot_ajax_views.check_update_request, name='bot-ajax-check_update'),
    path('end-session/', bot_ajax_views.end_session_request, name='bot-ajax-end_session'),
]

# url - /bot/...
bot_urls = [
    path('start/', bot_views.start_page, name='bot-start'),
    path('', bot_views.index_page, name='bot-index'),
    path('time-interval/', bot_views.time_interval_page, name='bot-time_interval'),
    path('action/', bot_views.bot_page, name='bot-action'),
    path('submit/', bot_views.submit_check_page, name='bot-submit'),
    path('bank/', bot_views.bank_page, name='bot-bank'),
    path('add-users/', bot_views.add_users_page, name='bot-add_users'),
    path('ajax/', include(bot_ajax_urls)),
    path('user/', bot_views.user_page_current, name='bot-user_page_current'),
    path('user/<int:settings_id>/', bot_views.user_page, name='bot-user_page'),
    path('all-time-intervals/', bot_views.all_time_intervals_page, name='bot-all_time_intervals_page'),
    path('all-bot-sessions/', bot_views.all_bot_sessions_page, name='bot-all_bot_sessions_page'),
    path('all-bank/', bot_views.all_bank_records_page, name='bot-all_bank_records_page'),
    path('session/<int:bot_id>/', bot_views.bot_view_page, name='bot-bot_view_page'),
]
