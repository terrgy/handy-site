from django.db import models
import random

from django.utils import timezone

from main.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=64,
        help_text='Tag display name',
        unique=True,
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    @staticmethod
    def get_all_tags_list() -> list:
        return [
            {
                'name': tag.name,
                'value': tag.pk,
            }
            for tag in Tag.objects.all()
        ]

    def __str__(self):
        return self.name


class Task(models.Model):
    _total_tasks = -1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nav_bar = True

    title = models.CharField(
        max_length=100,
        help_text='Main task name',
        verbose_name='title',
    )
    description = models.TextField(
        max_length=1000,
        help_text='Full description of the task',
        verbose_name='description',
    )
    link = models.URLField(
        help_text='URL to the testing system with the task',
        verbose_name='link',
        blank=True,
    )
    solutions_count = models.IntegerField(
        help_text='Number of successful solutions to this task',
        verbose_name='Solutions count',
        default=0,
    )
    last_solution = models.DateTimeField(
        help_text='Time of last successful solution to this task',
        verbose_name='last solve',
        default=timezone.now,
    )
    last_try = models.DateTimeField(
        help_text='Time of last solution attempt (successful or not)',
        verbose_name='last try',
        default=timezone.now,
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name='tags',
        help_text='Tags to this task',
    )

    def enable_nav_bar(self):
        self.nav_bar = True

    def disable_nav_bar(self):
        self.nav_bar = False

    def is_solved(self) -> bool:
        return self.solutions_count > 0

    def try_to_solve(self, save: bool = True):
        self.last_try = timezone.now()
        if save:
            self.save()

    def solve(self, save: bool = True):
        self.try_to_solve(save=False)
        self.solutions_count += 1
        self.last_solution = timezone.now()
        if save:
            self.save()

    @classmethod
    def get_total_count(cls) -> int:
        if cls._total_tasks == -1:
            cls._total_tasks = Task.objects.count()
        return cls._total_tasks

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class Training(models.Model):
    TRAINING_STATUSES = [
        (1, 'started'),
        (2, 'ended'),
    ]

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='training',
        help_text='Owner of the training',
        verbose_name='user',
    )
    status = models.IntegerField(
        choices=TRAINING_STATUSES,
        default=1,
    )

    def get_status(self) -> str:
        return self.get_status_display()

    def check_status(self, status) -> bool:
        if isinstance(status, int):
            return self.status == status
        return self.get_status_display() == status

    def get_current_training_task(self):
        training_task = self.tasks.all().first()
        if training_task is None:
            self.end_training()
        return training_task

    def get_current_task(self):
        training_task = self.get_current_training_task()
        if training_task is None:
            return None
        return training_task.task

    def next_task(self):
        training_task = self.get_current_training_task()
        if training_task is not None:
            training_task.delete()

    def end_training(self):
        self.status = 2
        self.save()

    @classmethod
    def start_new_training(cls, request):
        try:
            cls.objects.get(user=request.user).delete()
        except cls.DoesNotExist:
            pass

        permutation = [
            task
            for task in Task.objects.all()
        ]
        random.shuffle(permutation)

        new_training = cls.objects.create(user=request.user)
        for task in permutation:
            TrainingTask.objects.create(training=new_training, task=task)
        return new_training

    class Meta:
        verbose_name = 'Training'
        verbose_name_plural = 'Trainings'


class TrainingTask(models.Model):
    training = models.ForeignKey(
        to=Training,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text='Training related to this task',
    )
    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        related_name='training_usages',
        help_text='Task related to this record',
    )

    class Meta:
        verbose_name = 'Training task'
        verbose_name_plural = 'Training tasks'
