from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from bot.forms import EditSettingsForm, AddUsersForm
from bot.models import UserBotSettings, TimeInterval, BotSession, BankRecord, SessionHistory, ChangeLog, \
    NotCompleteIntervalPenalty, CheckFailPenalty
from main.models import User


@login_required
def start_page(request):
    if UserBotSettings.is_registered_in_bot(request.user):
        return redirect('bot-index')
    timezone.activate('Europe/Moscow')
    return render(request, 'pages/start_page.html')


@login_required
def index_page(request):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    timezone.activate('Europe/Moscow')
    context = dict()
    context['not_complete_interval_penalty'] = NotCompleteIntervalPenalty.get_last_penalty()
    context['check_fail_penalty'] = CheckFailPenalty.get_last_penalty()
    context['logs'] = ChangeLog.objects.all().order_by('time').reverse()
    return render(request, 'pages/bot_index_page.html', context)


@login_required
def time_interval_page(request):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    timezone.activate('Europe/Moscow')
    context = dict()
    interval = TimeInterval.get_running_time_interval(settings)
    if interval is not None:
        context['time_interval'] = interval
    context['other_time_intervals'] = TimeInterval.objects.filter(start_time__lte=timezone.now(),
                                                                  end_time__gte=timezone.now())
    context['time_intervals_history'] = TimeInterval.objects.filter(end_time__lt=timezone.now()).order_by(
        'end_time').reverse()[:10]
    return render(request, 'pages/time_interval_page.html', context)


@login_required()
def bot_page(request):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    timezone.activate('Europe/Moscow')
    context = dict()
    session = BotSession.get_session(settings)
    if session is not None:
        context['session'] = session
    context['other_sessions'] = BotSession.objects.all()
    context['sessions_history'] = SessionHistory.objects.all().order_by('end_time').reverse()[:10]
    return render(request, 'pages/bot_page.html', context)


@login_required()
def submit_check_page(request):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    timezone.activate('Europe/Moscow')
    session = BotSession.get_session(settings)
    if (session is None) or (not session.is_time_to_check()):
        return redirect('bot-action')
    return render(request, 'pages/submit_check_page.html')


@login_required()
def bank_page(request):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    timezone.activate('Europe/Moscow')
    context = dict()
    context['bank_sum'] = BankRecord.count_bank()
    context['settings'] = settings
    context['records'] = BankRecord.objects.all().order_by('time').reverse()[:10]
    return render(request, 'pages/bank_page.html', context)


@staff_member_required()
def add_users_page(request):
    if request.method == 'POST':
        form = AddUsersForm(request.POST)
        if form.is_valid():
            User.objects.create_user(form.cleaned_data['username'], '', form.cleaned_data['password'])
            messages.add_message(request, messages.SUCCESS, 'Успех!')
        else:
            messages.add_message(request, messages.ERROR, 'Ошибка')
    context = dict()
    context['add_users_form'] = AddUsersForm()
    return render(request, 'pages/add_users_page.html', context)


@login_required()
def user_page(request, settings_id):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')

    page_settings = get_object_or_404(UserBotSettings, pk=settings_id)

    timezone.activate('Europe/Moscow')
    context = dict()
    context['page_settings'] = page_settings
    if settings == page_settings:
        context['settings_form'] = EditSettingsForm(instance=settings)
    context['page_time_intervals'] = TimeInterval.objects.filter(user_bot_settings=page_settings).order_by('end_time').reverse()
    context['page_session_history'] = SessionHistory.objects.filter(user_bot_settings=page_settings).order_by('end_time').reverse()
    return render(request, 'pages/user_page.html', context)


@login_required()
def user_page_current(request):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    return redirect('bot-user_page', settings.pk)


@login_required
def all_time_intervals_page(request):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    timezone.activate('Europe/Moscow')
    context = dict()
    context['time_intervals_history'] = TimeInterval.objects.filter(end_time__lt=timezone.now()).order_by(
        'end_time').reverse()
    return render(request, 'pages/all_time_intervals_page.html', context)


@login_required
def all_bot_sessions_page(request):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    timezone.activate('Europe/Moscow')
    context = dict()
    context['sessions_history'] = SessionHistory.objects.all().order_by('end_time').reverse()
    return render(request, 'pages/all_bot_sessions_page.html', context)


@login_required()
def all_bank_records_page(request):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    timezone.activate('Europe/Moscow')
    context = dict()
    context['records'] = BankRecord.objects.all().order_by('time').reverse()
    return render(request, 'pages/all_bank_records_page.html', context)


@login_required()
def bot_view_page(request, bot_id):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    page_bot = get_object_or_404(SessionHistory, pk=bot_id)

    timezone.activate('Europe/Moscow')
    context = dict()
    context['page_bot'] = page_bot
    return render(request, 'pages/bot_view_page.html', context)


@login_required()
def time_interval_view_page(request, time_interval_id):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    page_time_interval = get_object_or_404(TimeInterval, pk=time_interval_id)

    timezone.activate('Europe/Moscow')
    context = dict()
    context['page_time_interval'] = page_time_interval
    context['page_bot_sessions'] = page_time_interval.get_sessions_on_time_interval()
    return render(request, 'pages/time_interval_view_page.html', context)
