from django.contrib import messages
from django.template.loader import render_to_string


def render_messages(request) -> str:
    return ''.join([
        render_to_string('base/messages/single_message_block.html', {'message': message})
        for message in messages.get_messages(request)
    ])
