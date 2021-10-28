from bot.models import TimeInterval


def bake_time_intervals():
    for interval in TimeInterval.objects.filter(status=TimeInterval.Statuses.RUNNING):
        interval.try_to_bake()
