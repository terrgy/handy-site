# Generated by Django 3.2.4 on 2021-10-31 17:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_auto_20211029_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.TextField(max_length=5000)),
                ('type', models.IntegerField(choices=[(1, 'System'), (2, 'Bug'), (3, 'Event'), (4, 'Community'), (5, 'Update')], default=1)),
            ],
            options={
                'verbose_name': 'Change log',
                'verbose_name_plural': 'Change logs',
            },
        ),
    ]
