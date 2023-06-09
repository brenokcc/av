# Generated by Django 4.1 on 2023-06-21 06:30

from django.db import migrations, models
import sloth.core.base
import sloth.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('av', '0016_validacao_qrcode_placa_dianteira_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultaAvulso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(0, 'Foto do Chassi'), (1, 'Foto Dianteira'), (2, 'Foto Traseira'), (3, 'Foto de Documento'), (4, 'Cor de Veículo')], verbose_name='Tipo')),
                ('foto', sloth.db.models.PhotoField(upload_to='', verbose_name='Foto')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('resultado', sloth.db.models.CharField(blank=True, max_length=255, null=True, verbose_name='Resultado')),
            ],
            options={
                'verbose_name': 'Consulta Avulso',
                'verbose_name_plural': 'Consultas Avulso',
            },
            bases=(models.Model, sloth.core.base.ModelMixin),
        ),
    ]
