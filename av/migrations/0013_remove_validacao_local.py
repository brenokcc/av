# Generated by Django 4.1 on 2023-06-09 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('av', '0012_validacao_local'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='validacao',
            name='local',
        ),
    ]
