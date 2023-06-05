# Generated by Django 4.1 on 2023-06-05 06:31

from django.db import migrations, models
import sloth.core.base
import sloth.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', sloth.db.models.BrCpfField(max_length=255, verbose_name='CPF')),
                ('nome', sloth.db.models.CharField(max_length=255, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
            },
            bases=(models.Model, sloth.core.base.ModelMixin),
        ),
        migrations.CreateModel(
            name='Validacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', sloth.db.models.BrCarPlateField(max_length=255, verbose_name='Número da Placa')),
                ('dianteira', models.BooleanField(default=False, verbose_name='Dianteira')),
                ('traseira', models.BooleanField(default=False, verbose_name='Traseira')),
                ('segunda_traseira', models.BooleanField(default=False, verbose_name='Segunda Traseira')),
                ('cpf_proprietario', sloth.db.models.BrCpfField(max_length=255, verbose_name='CPF do Proprietário')),
                ('nome_proprietario', sloth.db.models.BrCpfField(max_length=255, verbose_name='Nome do Proprietário')),
                ('foto_perfil_proprietario', sloth.db.models.BrCpfField(max_length=255, verbose_name='Foto de Perfil do Proprietário')),
                ('foto_documento_proprietario', sloth.db.models.BrCpfField(max_length=255, verbose_name='Foto do Documento do Proprietário')),
                ('cpf_representante', sloth.db.models.BrCpfField(max_length=255, verbose_name='CPF do Representante')),
                ('nome_representante', sloth.db.models.BrCpfField(max_length=255, verbose_name='Nome do Representante')),
                ('foto_perfil_representante', sloth.db.models.BrCpfField(max_length=255, verbose_name='Foto de Perfil do Representante')),
                ('foto_documento_representante', sloth.db.models.BrCpfField(max_length=255, verbose_name='Foto do Documento do Representante')),
                ('foto_procuracao', sloth.db.models.BrCpfField(max_length=255, verbose_name='Foto da Procuração')),
                ('foto_chassi_veiculo', sloth.db.models.PhotoField(blank=True, null=True, upload_to='', verbose_name='Foto do Chassi do Veículo')),
                ('foto_dianteira_veiculo', sloth.db.models.PhotoField(blank=True, null=True, upload_to='', verbose_name='Foto Dianteira do Veículo')),
                ('foto_traseira_veiculo', sloth.db.models.PhotoField(blank=True, null=True, upload_to='', verbose_name='Foto Traseira do Veículo')),
                ('foto_placa_dianteira', sloth.db.models.PhotoField(blank=True, null=True, upload_to='', verbose_name='Foto da Placa Dianteira')),
                ('foto_placa_traseira', sloth.db.models.PhotoField(blank=True, null=True, upload_to='', verbose_name='Foto da Placa Traseira')),
                ('foto_segunda_placa_traseira', sloth.db.models.PhotoField(blank=True, null=True, upload_to='', verbose_name='Foto da Segunda Placa Traseira')),
                ('foto_boletim_ocorrencia', sloth.db.models.PhotoField(blank=True, null=True, upload_to='', verbose_name='Foto do Boletim de Ocorrência')),
                ('foto_descarte_placa_dianteira', sloth.db.models.PhotoField(blank=True, null=True, upload_to='', verbose_name='Foto do Descarte da Placa Dianteira')),
                ('foto_descarte_placa_traseira', sloth.db.models.PhotoField(blank=True, null=True, upload_to='', verbose_name='Foto do Descarte da Placa Traseira')),
                ('foto_descarte_segunda_placa_traseira', sloth.db.models.PhotoField(blank=True, null=True, upload_to='', verbose_name='Foto do Descarte da Segunda Placa Traseira')),
            ],
            options={
                'verbose_name': 'Validação',
                'verbose_name_plural': 'Validações',
                'fieldsets': {'Dados da Placa': ('placa', 'dianteira', 'traseira', 'segunda_traseira'), 'Descarte': ('foto_boletim_ocorrencia', 'foto_descarte_placa_dianteira', 'foto_descarte_placa_traseira', 'foto_descarte_segunda_placa_traseira'), 'Proprietário': ('cpf_proprietario', 'nome_proprietario', 'foto_perfil_proprietario', 'foto_documento_proprietario'), 'Representante': ('cpf_representante', 'nome_representante', 'foto_perfil_representante', 'foto_documento_representante', 'foto_procuracao'), 'Veículo': ('foto_chassi_veiculo', 'foto_dianteira_veiculo', 'foto_traseira_veiculo', '', 'foto_placa_dianteira', 'foto_placa_traseira', 'foto_segunda_placa_traseira')},
            },
            bases=(models.Model, sloth.core.base.ModelMixin),
        ),
    ]
