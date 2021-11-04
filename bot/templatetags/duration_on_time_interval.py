from django.template.defaulttags import register

from bot.models import TimeInterval, SessionHistory
from bot.templatetags.duration import duration


@register.simple_tag()
def duration_on_time_interval(time_interval: TimeInterval, session: SessionHistory):
    return duration(session.get_duration_on_interval(time_interval.start_time, time_interval.end_time))
