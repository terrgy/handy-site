from bot.models import BotSession


def verify_sessions():
    for session in BotSession.objects.all():
        session.verify_session()
