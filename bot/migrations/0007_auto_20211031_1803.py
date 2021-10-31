# Generated by Django 3.2.4 on 2021-10-31 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_auto_20211031_1755'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basepenalty',
            options={'ordering': ['time'], 'verbose_name': 'Base penalty', 'verbose_name_plural': 'Base penalties'},
        ),
        migrations.AlterModelOptions(
            name='checkfailpenalty',
            options={'verbose_name': 'Check fail penalty', 'verbose_name_plural': 'Check fail penalties'},
        ),
        migrations.AlterModelOptions(
            name='notcompleteintervalpenalty',
            options={'verbose_name': 'Not complete interval penalty', 'verbose_name_plural': 'Not complete interval penalties'},
        ),
    ]
