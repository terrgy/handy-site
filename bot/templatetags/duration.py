from datetime import timedelta

from django.template.defaulttags import register
from django.template.loader import render_to_string


@register.simple_tag()
def duration(delta: timedelta, with_days=False):
    if delta.days < 0:
        return render_to_string('blocks/negative_duration.html')
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60
    hours = delta.seconds // 3600
    if with_days:
        return '{days:d}:{hours:02d}:{minutes:02d}:{seconds:02d}'.format(
            days=delta.days,
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )
    return '{hours:02d}:{minutes:02d}:{seconds:02d}'.format(
        hours=hours + delta.days * 24,
        minutes=minutes,
        seconds=seconds,
    )
