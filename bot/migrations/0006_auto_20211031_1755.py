# Generated by Django 3.2.4 on 2021-10-31 17:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_changelog'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasePenalty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['time'],
            },
        ),
        migrations.AlterField(
            model_name='changelog',
            name='type',
            field=models.IntegerField(choices=[(1, 'System'), (2, 'Bug'), (3, 'Event'), (4, 'Community'), (5, 'Update'), (6, 'Undefined')], default=1),
        ),
        migrations.CreateModel(
            name='CheckFailPenalty',
            fields=[
                ('basepenalty_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bot.basepenalty')),
            ],
            bases=('bot.basepenalty', models.Model),
        ),
        migrations.CreateModel(
            name='NotCompleteIntervalPenalty',
            fields=[
                ('basepenalty_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bot.basepenalty')),
            ],
            bases=('bot.basepenalty', models.Model),
        ),
    ]