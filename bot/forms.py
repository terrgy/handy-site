from django.forms import ModelForm, Form, CharField

from bot.models import UserBotSettings


class EditSettingsForm(ModelForm):
    class Meta:
        model = UserBotSettings
        fields = ['study_plan_hours', 'study_plan_days_duration_time_interval',
                  'self_check_mode', 'time_interval_auto_renewal', ]
        labels = {
            'self_check_mode': 'Режим самопроверки',
            'time_interval_auto_renewal': 'Автоматический перезапуск отчетного периода',
            'study_plan_hours': 'Цель на отчетный период',
            'study_plan_days_duration_time_interval': 'Длительность отчетного периода'
        }
        help_texts = {
            'self_check_mode': 'Включите этот режим, если нет возможности постоянно держать окно браузера открытым ('
                               'проверка через дискорд) ',
            'study_plan_hours': 'Сколько планируете ботать в часах?',
            'study_plan_days_duration_time_interval': 'В днях',
        }


class AddUsersForm(Form):
    username = CharField(max_length=100)
    password = CharField(max_length=100)
