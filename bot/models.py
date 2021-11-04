from datetime import timedelta
from random import randint

from django.db import models
from django.utils import timezone

from main.models import User


class UserBotSettings(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )

    is_active = models.BooleanField(
        default=True,
    )

    points = models.IntegerField(
        default=0
    )

    self_check_mode = models.BooleanField(
        default=False,
        help_text='Enable this mode if user cant check himself in browser',
    )

    time_interval_auto_renewal = models.BooleanField(
        default=True,
    )

    study_plan_hours = models.PositiveSmallIntegerField(
        help_text='Amount of hours during user plans to study in specified time interval',
        default=0,

    )

    study_plan_days_duration_time_interval = models.PositiveSmallIntegerField(
        help_text='Amount of days in one time interval',
        default=0,
    )

    MAX_TIME_INTERVAL = 31

    class Meta:
        verbose_name = 'User bot settings'
        verbose_name_plural = 'Users bot settings'

    class AlreadyRegisteredError(Exception):
        pass

    class TimeIntervalAlreadyStartedError(Exception):
        pass

    class RegistrationParametersError(Exception):
        pass

    class PlanMoreThanIntervalError(Exception):
        pass

    class StudyPlanNotAssignedError(Exception):
        pass

    @classmethod
    def get_settings(cls, user):
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return None

    @classmethod
    def is_registered_in_bot(cls, user):
        return cls.objects.filter(user=user).exists()

    @classmethod
    def register_new_user(cls, user):
        if cls.is_registered_in_bot(user):
            raise cls.AlreadyRegisteredError()
        return cls.objects.create(
            user=user,
        )

    def deposit_points(self, points):
        self.points += points
        self.save()

    def withdraw_points(self, points):
        self.points -= points
        self.save()

    def start_new_time_interval(self) -> 'TimeInterval':
        if TimeInterval.is_time_interval_running(self):
            raise self.TimeIntervalAlreadyStartedError()
        if not self.study_plan_days_duration_time_interval:
            raise self.StudyPlanNotAssignedError()
        return TimeInterval.objects.create(
            user_bot_settings=self,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(days=self.study_plan_days_duration_time_interval),
            initial_duration=self.study_plan_days_duration_time_interval,
            hours_target=self.study_plan_hours,
        )

    def get_bank_intake(self) -> int:
        return BankRecord.count_user_intake(self)

    def get_bank_profit(self) -> int:
        return BankRecord.count_user_profit(self)

    def __str__(self):
        return '{} (bs)'.format(self.user)


class TimeInterval(models.Model):
    user_bot_settings = models.ForeignKey(
        to=UserBotSettings,
        on_delete=models.CASCADE
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    initial_duration = models.PositiveSmallIntegerField(
        null=False,
    )

    hours_target = models.PositiveSmallIntegerField(
        null=False,
    )

    hours_completed = models.PositiveSmallIntegerField(
        default=0,
    )

    penalty = models.IntegerField(
        default=0,
    )

    class Statuses(models.IntegerChoices):
        RUNNING = 1
        COMPLETED = 2
        FAILED = 3
        ON_HOLD = 4
        TERMINATED_WITH_REFUND = 5
        TERMINATED_WITHOUT_REFUND = 6
        TERMINATED_PREMATURE = 7

    status = models.IntegerField(
        choices=Statuses.choices,
        default=1,
    )

    class Meta:
        verbose_name = 'Time interval'
        verbose_name_plural = 'Time intervals'

    @classmethod
    def is_time_interval_running(cls, user_bot_settings: UserBotSettings) -> bool:
        return cls.objects.filter(user_bot_settings=user_bot_settings,
                                  start_time__lte=timezone.now(), end_time__gte=timezone.now()).exists()

    @classmethod
    def get_running_time_interval(cls, user_bot_settings: UserBotSettings) -> 'TimeInterval':
        try:
            return cls.objects.get(user_bot_settings=user_bot_settings,
                                   start_time__lte=timezone.now(), end_time__gte=timezone.now())
        except cls.DoesNotExist:
            return None

    def get_real_duration(self) -> timedelta:
        return self.end_time - self.start_time

    def get_sessions_on_time_interval(self):
        return SessionHistory.get_sessions_on_time_interval(self.user_bot_settings, self.start_time, self.end_time)

    def get_sum_durations_on_time_interval(self) -> timedelta:
        return SessionHistory.get_durations_sum_in_time_interval(self.user_bot_settings, self.start_time, self.end_time)

    def count_completed_hours(self) -> int:
        completed_delta = self.get_sum_durations_on_time_interval()
        self.hours_completed = completed_delta.days * 24 + completed_delta.seconds // 3600
        return self.hours_completed

    def assign_penalty(self):
        if self.hours_completed >= self.hours_target:
            return
        self.penalty = NotCompleteIntervalPenalty.get_last_penalty() * self.initial_duration * (self.hours_target - self.hours_completed) // self.hours_target
        self.save()

        BankRecord.objects.create(
            user_bot_settings=self.user_bot_settings,
            value=self.penalty,
            reason=BankRecord.Reasons.TIME_INTERVAL_FAIL,
        )

        self.user_bot_settings.withdraw_points(self.penalty)

    def renew_time_interval(self) -> bool:
        if not self.user_bot_settings.time_interval_auto_renewal:
            return False

        try:
            self.user_bot_settings.start_new_time_interval()
        except (UserBotSettings.TimeIntervalAlreadyStartedError, UserBotSettings.StudyPlanNotAssignedError):
            return False
        return True

    def try_to_bake(self) -> bool:
        if self.status not in [self.Statuses.RUNNING, self.Statuses.TERMINATED_PREMATURE]:
            return False
        if timezone.now() <= self.end_time:
            return False
        if BotSession.is_running_session(self.user_bot_settings):
            return False

        if self.status != self.Statuses.TERMINATED_PREMATURE:
            self.renew_time_interval()

        self.count_completed_hours()
        if self.hours_completed >= self.hours_target:
            self.status = self.Statuses.COMPLETED
        else:
            self.status = self.Statuses.FAILED
        self.assign_penalty()
        self.save()

        return True

    def __str__(self):
        return '{}: {} - {}'.format(self.user_bot_settings, self.start_time, self.end_time)


class SessionHistory(models.Model):
    user_bot_settings = models.ForeignKey(
        to=UserBotSettings,
        on_delete=models.CASCADE,
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField(
        default=timezone.now
    )

    class EndingCauses(models.IntegerChoices):
        MANUAL = 1
        CHECK_FAILURE = 2

    ending_cause = models.IntegerField(
        choices=EndingCauses.choices,
    )

    class Meta:
        verbose_name = 'Session history'
        verbose_name_plural = 'Sessions histories'

    def get_duration_on_interval(self, start, end) -> timedelta:
        left_border = self.start_time
        if start > left_border:
            left_border = start

        right_border = self.end_time
        if end < right_border:
            right_border = end

        if right_border < left_border:
            return timedelta()
        return right_border - left_border

    def get_duration(self) -> timedelta:
        return self.end_time - self.start_time

    @classmethod
    def get_durations_sum_in_time_interval(cls, user_bot_settings: UserBotSettings, start, end) -> timedelta:
        durations_sum = timedelta()
        for session in cls.get_sessions_on_time_interval(user_bot_settings, start, end):
            durations_sum += session.get_duration_on_interval(start, end)
        return durations_sum

    @classmethod
    def get_sessions_on_time_interval(cls, user_bot_settings: UserBotSettings, start, end):
        return cls.objects.filter(user_bot_settings=user_bot_settings, start_time__lte=end, end_time__gte=start)


class BotSession(models.Model):
    user_bot_settings = models.OneToOneField(
        to=UserBotSettings,
        on_delete=models.CASCADE,
    )

    start_time = models.DateTimeField(
        default=timezone.now,
    )

    self_check_mode = models.BooleanField(
        default=False,
    )

    next_check_time = models.DateTimeField(
        null=True,
    )

    class Meta:
        verbose_name = 'Bot session'
        verbose_name_plural = 'Bot sessions'

    MIN_NEXT_CHECK_TIME_INTERVAL = 20
    MAX_NEXT_CHECK_TIME_INTERVAL = 60

    def generate_new_check_time(self):
        minutes_to_next_check = randint(self.MIN_NEXT_CHECK_TIME_INTERVAL, self.MAX_NEXT_CHECK_TIME_INTERVAL)
        delta = timedelta(minutes=minutes_to_next_check)
        self.next_check_time = timezone.now() + delta

    AVAILABLE_CHECK_TIME_DURATION = 5

    def is_time_to_check(self):
        if self.self_check_mode:
            return False
        return (self.next_check_time <= timezone.now()) and \
               (timezone.now() <= self.next_check_time + timedelta(minutes=self.AVAILABLE_CHECK_TIME_DURATION))

    def is_check_overdue(self):
        if self.self_check_mode:
            return False
        return self.next_check_time + timedelta(minutes=self.AVAILABLE_CHECK_TIME_DURATION) < timezone.now()

    @classmethod
    def is_running_session(cls, user_bot_settings: UserBotSettings):
        return cls.objects.filter(user_bot_settings=user_bot_settings).exists()

    @classmethod
    def get_session(cls, user_bot_settings: UserBotSettings):
        try:
            return cls.objects.get(user_bot_settings=user_bot_settings)
        except cls.DoesNotExist:
            return None

    @classmethod
    def start_new_session(cls, user_bot_settings: UserBotSettings):
        session = cls(user_bot_settings=user_bot_settings, self_check_mode=user_bot_settings.self_check_mode)
        if not session.self_check_mode:
            session.generate_new_check_time()
        session.save()
        return session

    def end_session(self, cause=SessionHistory.EndingCauses.MANUAL):
        SessionHistory.objects.create(
            user_bot_settings=self.user_bot_settings,
            start_time=self.start_time,
            ending_cause=cause,
        )
        self.delete()

    def verify_session(self):
        if not self.self_check_mode:
            if self.is_check_overdue():
                self.end_session(SessionHistory.EndingCauses.CHECK_FAILURE)
                penalty = CheckFailPenalty.get_last_penalty()
                BankRecord.objects.create(
                    user_bot_settings=self.user_bot_settings,
                    value=penalty,
                    reason=BankRecord.Reasons.CHECK_FAIL,
                )
                self.user_bot_settings.withdraw_points(penalty)

    def process_check(self):
        if self.is_time_to_check():
            self.generate_new_check_time()
            self.save()


class TerminationApplication(models.Model):
    time_interval = models.OneToOneField(
        to=TimeInterval,
        on_delete=models.CASCADE,
    )

    class Statuses(models.IntegerChoices):
        REVIEWING = 1
        ACCEPTED_REFUND = 2
        DECLINED_REFUND = 3

    status = models.IntegerField(
        choices=Statuses.choices,
        default=1,
    )

    message = models.TextField(
        max_length=1000,
        blank=True,
    )

    reply = models.TextField(
        max_length=1000,
        blank=True,
    )

    class Meta:
        verbose_name = 'Termination application'
        verbose_name_plural = 'Termination applications'

    @staticmethod
    def premature_termination(time_interval: TimeInterval):
        time_interval.end_time = timezone.now()
        time_interval.status = time_interval.Statuses.TERMINATED_PREMATURE
        time_interval.save()

    @classmethod
    def add_application(cls, time_interval: TimeInterval, message) -> 'TerminationApplication':
        time_interval.end_time = timezone.now()
        time_interval.status = time_interval.Statuses.ON_HOLD
        time_interval.save()

        return cls.objects.create(
            time_interval=time_interval,
            message=message,
        )

    def accept_refund(self, reply):
        self.time_interval.count_completed_hours()
        self.time_interval.status = TimeInterval.Statuses.TERMINATED_WITH_REFUND
        self.time_interval.save()

        self.status = self.Statuses.ACCEPTED_REFUND
        self.reply = reply
        self.save()

    def decline_refund(self, reply):
        self.time_interval.count_completed_hours()
        self.time_interval.status = TimeInterval.Statuses.TERMINATED_WITHOUT_REFUND
        self.time_interval.assign_penalty()
        self.time_interval.save()

        self.status = self.Statuses.DECLINED_REFUND
        self.reply = reply
        self.save()


class BankRecord(models.Model):
    user_bot_settings = models.ForeignKey(
        to=UserBotSettings,
        on_delete=models.CASCADE,
    )

    time = models.DateTimeField(
        default=timezone.now,
    )

    value = models.IntegerField(
        default=0
    )

    class Reasons(models.IntegerChoices):
        CHECK_FAIL = 1
        TIME_INTERVAL_FAIL = 2

    reason = models.IntegerField(
        choices=Reasons.choices,
    )

    class Meta:
        verbose_name = 'Bank record'
        verbose_name_plural = 'Bank records'

    @classmethod
    def count_bank(cls) -> int:
        values_sum = 0
        for record in cls.objects.all():
            values_sum += record.value
        return values_sum

    @classmethod
    def count_user_intake(cls, user_bot_settings: UserBotSettings) -> int:
        values_sum = 0
        for record in cls.objects.filter(user_bot_settings=user_bot_settings):
            values_sum += record.value
        return values_sum

    @classmethod
    def count_user_profit(cls, user_bot_settings: UserBotSettings) -> int:
        users_count = UserBotSettings.objects.filter(is_active=True).count() - 1
        if not users_count:
            return 0
        values_sum = 0
        for record in cls.objects.exclude(user_bot_settings=user_bot_settings):
            values_sum += record.value
        values_sum = values_sum // users_count
        return values_sum


class ChangeLog(models.Model):
    time = models.DateTimeField(
        default=timezone.now
    )

    message = models.TextField(
        max_length=5000,
    )

    class Types(models.IntegerChoices):
        SYSTEM = 1
        BUG = 2
        EVENT = 3
        COMMUNITY = 4
        UPDATE = 5
        UNDEFINED = 6

    type = models.IntegerField(
        choices=Types.choices,
        default=1,
    )

    class Meta:
        verbose_name = 'Change log'
        verbose_name_plural = 'Change logs'

    def verbose_ru_translation(self) -> str:
        if self.type == self.Types.SYSTEM:
            return 'Системное'
        elif self.type == self.Types.BUG:
            return 'Исправление'
        elif self.type == self.Types.EVENT:
            return 'Событие'
        elif self.type == self.Types.COMMUNITY:
            return 'Сообщество'
        elif self.type == self.Types.UPDATE:
            return 'Обновление'
        elif self.type == self.Types.UNDEFINED:
            return 'Неопределенное'
        return ''


class BasePenalty(models.Model):
    DEFAULT_VALUE = 0

    value = models.IntegerField(
        default=DEFAULT_VALUE,
    )

    time = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        ordering = ['time']
        verbose_name = 'Base penalty'
        verbose_name_plural = 'Base penalties'

    @classmethod
    def get_last_penalty(cls) -> int:
        try:
            return cls.objects.reverse()[0:1].get().value
        except cls.DoesNotExist:
            return cls.DEFAULT_VALUE


class NotCompleteIntervalPenalty(BasePenalty):
    DEFAULT_VALUE = 1000

    class Meta:
        verbose_name = 'Not complete interval penalty'
        verbose_name_plural = 'Not complete interval penalties'


class CheckFailPenalty(BasePenalty):
    DEFAULT_VALUE = 100

    class Meta:
        verbose_name = 'Check fail penalty'
        verbose_name_plural = 'Check fail penalties'
