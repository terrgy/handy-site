from django.utils import timezone

from bot.models import TimeInterval


def bake_time_intervals():
    for interval in TimeInterval.objects.filter(status__in=[TimeInterval.Statuses.RUNNING, TimeInterval.Statuses.TERMINATED_PREMATURE], end_time__lt=timezone.now()):
        interval.try_to_bake()
