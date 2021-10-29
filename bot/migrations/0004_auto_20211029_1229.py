# Generated by Django 3.2.4 on 2021-10-29 12:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('bot', '0003_auto_20211028_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='botsession',
            name='self_check_mode',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='botsession',
            name='next_check_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='terminationapplication',
            name='message',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='terminationapplication',
            name='reply',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]