# Generated by Django 3.2.4 on 2021-10-28 17:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('bot', '0002_auto_20211028_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeinterval',
            name='status',
            field=models.IntegerField(
                choices=[(1, 'Running'), (2, 'Completed'), (3, 'Failed'), (4, 'On Hold'), (5, 'Terminated With Refund'),
                         (6, 'Terminated Without Refund')], default=1),
        ),
        migrations.CreateModel(
            name='BankRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('value', models.IntegerField(default=0)),
                ('reason', models.IntegerField(choices=[(1, 'Check Fail'), (2, 'Time Interval Fail')])),
                ('user_bot_settings',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.userbotsettings')),
            ],
            options={
                'verbose_name': 'Bank record',
                'verbose_name_plural': 'Bank records',
            },
        ),
    ]
