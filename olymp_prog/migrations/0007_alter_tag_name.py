# Generated by Django 3.2.4 on 2021-06-18 17:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('olymp_prog', '0006_auto_20210614_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='Tag display name', max_length=64, unique=True),
        ),
    ]
