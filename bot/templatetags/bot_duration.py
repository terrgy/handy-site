from django.template.defaulttags import register
from django.template.loader import render_to_string

from bot.models import SessionHistory


@register.simple_tag()
def bot_duration(session: SessionHistory):
    duration = session.get_duration()
    if duration.days < 0:
        return render_to_string('blocks/negative_duration.html')
    return '{hours:02d}:{minutes:02d}:{seconds:02d}'.format(
        hours=duration.days * 24 + duration.seconds // 3600,
        minutes=(duration.seconds % 3600) // 60,
        seconds=duration.seconds % 60,
    )
