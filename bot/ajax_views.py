from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse

from bot.forms import EditSettingsForm
from bot.models import UserBotSettings, TimeInterval, TerminationApplication, BotSession
from main.utils.get_json_error import get_json_error
from main.utils.get_json_response import get_json_response


@login_required
def register_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    UserBotSettings.register_new_user(request.user)
    return get_json_response(request, redirect=reverse('bot-settings'))


@login_required()
def edit_settings_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        raise PermissionDenied
    form = EditSettingsForm(instance=settings, data=request.POST)
    if not form.is_valid():
        messages.add_message(request, messages.ERROR, 'Неверные параметры')
        return get_json_error(request)
    hours = int(form.cleaned_data['study_plan_hours'])
    days = int(form.cleaned_data['study_plan_days_duration_time_interval'])
    if days > UserBotSettings.MAX_TIME_INTERVAL:
        messages.add_message(request, messages.ERROR, 'Максимальная длительность отчетного периода - 31 день')
        return get_json_error(request)
    if days <= 0:
        messages.add_message(request, messages.ERROR, 'Длительность не может быть нулевой')
        return get_json_error(request)
    if hours <= 0:
        messages.add_message(request, messages.ERROR, 'Цель не может быть нулевой')
        return get_json_error(request)
    if days * 24 < hours:
        messages.add_message(request, messages.ERROR, 'Цель превышает отчетный период')
        return get_json_error(request)
    form.save()
    messages.add_message(request, messages.SUCCESS, 'Сохранено')
    return get_json_response(request)


@login_required()
def start_time_interval_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        raise PermissionDenied
    if TimeInterval.is_time_interval_running(settings):
        messages.add_message(request, messages.ERROR, 'Отчетный период уже идет')
        return get_json_error(request)

    try:
        settings.start_new_time_interval()
    except UserBotSettings.StudyPlanNotAssignedError:
        messages.add_message(request, messages.ERROR, 'Не заданы параметры отчетного периода')
        return get_json_error(request)
    return get_json_response(request, redirect=reverse('bot-time_interval'))


@login_required()
def premature_termination_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        raise PermissionDenied

    interval = TimeInterval.get_running_time_interval(settings)
    if interval is None:
        messages.add_message(request, messages.ERROR, 'Отчетный период не идет')
        return get_json_error(request)

    TerminationApplication.premature_termination(interval)
    return get_json_response(request, redirect=reverse('bot-time_interval'))


@login_required()
def start_bot_session_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        raise PermissionDenied
    if BotSession.is_running_session(settings):
        messages.add_message(request, messages.ERROR, 'Бот уже идет')
        return get_json_error(request)

    BotSession.start_new_session(settings)
    return get_json_response(request, redirect=reverse('bot-action'))


@login_required()
def check_update_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        raise PermissionDenied
    session = BotSession.get_session(settings)
    if session is None:
        return get_json_response(request, check=False, check_redirect=reverse('bot-action'))
    if session.is_time_to_check():
        return get_json_response(request, check=True, check_redirect=reverse('bot-submit'))
    return get_json_error(request, check=False, check_redirect=reverse('bot-action'))


@login_required()
def submit_check_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        raise PermissionDenied
    session = BotSession.get_session(settings)
    if session is None:
        messages.add_message(request, messages.ERROR, 'Бот не идет')
        return get_json_error(request)
    if not session.is_time_to_check():
        messages.add_message(request, messages.ERROR, 'Сейчас не время проверки')
        return get_json_error(request)
    session.process_check()
    return get_json_error(request, redirect=reverse('bot-action'))


@login_required()
def end_session_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        raise PermissionDenied
    session = BotSession.get_session(settings)
    if session is None:
        messages.add_message(request, messages.ERROR, 'Бот и так не идет')
        return get_json_error(request)
    session.end_session()
    return get_json_error(request, redirect=reverse('bot-action'))
