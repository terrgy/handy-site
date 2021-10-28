from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# Create your views here.
from django.utils import timezone

from bot.forms import EditSettingsForm
from bot.models import UserBotSettings, TimeInterval, BotSession, BankRecord


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


@login_required
def settings_page(request):
    settings = UserBotSettings.get_settings(request.user)
    if settings is None:
        return redirect('bot-start')
    timezone.activate('Europe/Moscow')
    context = dict()
    context['settings'] = settings
    context['settings_form'] = EditSettingsForm(instance=settings)
    return render(request, 'pages/settings_page.html', context)


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
                                                                  end_time__gte=timezone.now()).exclude(
        user_bot_settings=settings)
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
    context['other_sessions'] = BotSession.objects.exclude(user_bot_settings=settings)
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
    context['bank_records'] = BankRecord.objects.all()
    return render(request, 'pages/bank_page.html', context)
