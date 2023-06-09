# Generated by Django 4.1 on 2023-06-07 06:30

from django.db import migrations, models
import django.db.models.deletion
import sloth.core.base
import sloth.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('av', '0004_validacao_chassi_validacao_cor_validacao_marca'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', sloth.db.models.CharField(max_length=255, verbose_name='Tipo')),
                ('data_hora', models.DateTimeField(verbose_name='Data/Hora')),
                ('valor', sloth.db.models.CharField(max_length=255, verbose_name='Valor')),
                ('observacao', sloth.db.models.CharField(max_length=255, null=True, verbose_name='Observação')),
                ('validacao', sloth.db.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='av.validacao', verbose_name='Validação')),
            ],
            options={
                'verbose_name': 'Consulta',
                'verbose_name_plural': 'Consultas',
            },
            bases=(models.Model, sloth.core.base.ModelMixin),
        ),
    ]
