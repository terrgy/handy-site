from django.db import models

from main.models import User


class Task(models.Model):
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
        verbose_name='link'
    )

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class Training(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='training',
        help_text='Owner of the training',
        verbose_name='user',
    )
    random_seed = models.PositiveBigIntegerField(
        help_text='Seed for the random generator that produces tasks permutation',
        verbose_name='random seed',
    )
    current_task = models.IntegerField(
        help_text='Current index of task being solved',
        verbose_name='current task index',
    )

    class Meta:
        verbose_name = 'Training'
        verbose_name_plural = 'Trainings'

