# Generated by Django 4.1 on 2023-06-10 15:20

from django.db import migrations
import sloth.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('av', '0015_alter_operador_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='validacao',
            name='qrcode_placa_dianteira',
            field=sloth.db.models.TextField(blank=True, null=True, verbose_name='Foto da Placa Dianteira'),
        ),
        migrations.AddField(
            model_name='validacao',
            name='qrcode_placa_traseira',
            field=sloth.db.models.TextField(blank=True, null=True, verbose_name='Foto da Placa Traseira'),
        ),
        migrations.AddField(
            model_name='validacao',
            name='qrcode_segunda_placa_traseira',
            field=sloth.db.models.TextField(blank=True, null=True, verbose_name='Foto da Segunda Placa Traseira'),
        ),
    ]