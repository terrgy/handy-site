# Generated by Django 3.2.4 on 2021-06-07 12:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('olymp_prog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user',
                 models.OneToOneField(help_text='Owner of the training', on_delete=django.db.models.deletion.CASCADE,
                                      related_name='training', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Training',
                'verbose_name_plural': 'Trainings',
            },
        ),
        migrations.CreateModel(
            name='TrainingTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task',
                 models.ForeignKey(help_text='Task related to this record', on_delete=django.db.models.deletion.CASCADE,
                                   related_name='training_usages', to='olymp_prog.task')),
                ('training', models.ForeignKey(help_text='Training related to this task',
                                               on_delete=django.db.models.deletion.CASCADE, related_name='tasks',
                                               to='olymp_prog.training')),
            ],
            options={
                'verbose_name': 'Training task',
                'verbose_name_plural': 'Training tasks',
            },
        ),
        migrations.DeleteModel(
            name='Trainings',
        ),
    ]
