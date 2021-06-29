import random

from django.db import models
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
    shuffle_methods = []

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
        blank=True,
    )
    link = models.URLField(
        help_text='URL to the testing system with the task',
        verbose_name='link',
        blank=True,
    )
    attempts_count = models.IntegerField(
        help_text='Number of solution attempts to this task',
        default=0,
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
    notes = models.TextField(
        help_text='Additional info about task',
        blank=True,
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name='tags',
        help_text='Tags to this task',
        blank=True,
    )

    def enable_nav_bar(self):
        self.nav_bar = True

    def disable_nav_bar(self):
        self.nav_bar = False

    def is_solved(self) -> bool:
        return self.solutions_count > 0

    def solution_rating(self) -> float:
        if self.attempts_count:
            return self.solutions_count * 100 / self.attempts_count
        return 0.0

    def try_to_solve(self, save: bool = True):
        self.attempts_count += 1
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

    @classmethod
    def filter_tasks(cls, tasks=None, **kwargs):
        if tasks is None:
            tasks = cls.objects.all()
        if ('tags' in kwargs) and kwargs['tags']:
            tasks = tasks.filter(tags__in=kwargs['tags'])
        if ('title' in kwargs) and kwargs['title']:
            tasks = tasks.filter(title__contains=kwargs['title'])
        if ('link' in kwargs) and kwargs['link']:
            tasks = tasks.exclude(link='').filter(link__isnull=False)
        return tasks

    @classmethod
    def simple_shuffle(cls, tasks=None):
        if tasks is None:
            tasks = cls.objects.all()
        permutation = [
            task
            for task in tasks
        ]
        random.shuffle(permutation)
        return permutation

    @classmethod
    def latest_solve_priority_shuffle(cls, tasks=None):
        if tasks is None:
            tasks = cls.objects.all()
        tasks = tasks.order_by('last_solution')
        permutation = [
            task
            for task in tasks
        ]
        block_size = max(int(len(permutation) * 0.05), 5)
        for i in range(0, len(permutation), block_size):
            tasks_slice = permutation[i: i + block_size]
            random.shuffle(tasks_slice)
            for j in range(len(tasks_slice)):
                permutation[i + j] = tasks_slice[j]
        return permutation

    @classmethod
    def get_shuffle_methods_choices(cls):
        return [
            (i, cls.shuffle_methods[i][0])
            for i in range(len(cls.shuffle_methods))
        ]

    @classmethod
    def get_shuffle_method(cls, index=0):
        return cls.shuffle_methods[index][1]

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


Task.shuffle_methods = [
    ('Simple shuffle', Task.simple_shuffle),
    ('Latest solve priority', Task.latest_solve_priority_shuffle),
]


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
    def start_new_training(cls, request, tasks=None):
        try:
            cls.objects.get(user=request.user).delete()
        except cls.DoesNotExist:
            pass

        if tasks is None:
            tasks = Task.objects.all()

        new_training = cls.objects.create(user=request.user)
        for task in tasks:
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
