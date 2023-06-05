from sloth.db import models, role, meta
from .roles import ADM


class AdministradorManager(models.Manager):

    def all(self):
        return self


@role(ADM, username='cpf')
class Administrador(models.Model):
    cpf = models.BrCpfField('CPF')
    nome = models.CharField('Nome')

    objects = AdministradorManager()

    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

    def __str__(self):
        return '{}'.format(self.pk)

    def has_permission(self, user):
        return user.is_superuser


class ValidacaoManager(models.Manager):
    def all(self):
        return self.lookups(ADM).display('placa', 'cpf_proprietario', 'nome_proprietario')

 
class Validacao(models.Model):
    placa = models.BrCarPlateField('Número da Placa')
    dianteira = models.BooleanField('Dianteira', default=False)
    traseira = models.BooleanField('Traseira', default=False)
    segunda_traseira = models.BooleanField('Segunda Traseira', default=False)

    cpf_proprietario = models.BrCpfField('CPF do Proprietário')
    nome_proprietario = models.CharField('Nome do Proprietário')
    foto_perfil_proprietario = models.PhotoField('Foto de Perfil do Proprietário', null=True, blank=True, upload_to='fotos')
    foto_documento_proprietario = models.PhotoField('Foto do Documento do Proprietário', null=True, blank=True, upload_to='fotos')

    cpf_representante = models.BrCpfField('CPF do Representante', null=True, blank=True)
    nome_representante = models.CharField('Nome do Representante', null=True, blank=True)
    foto_perfil_representante = models.PhotoField('Foto de Perfil do Representante', null=True, blank=True, upload_to='fotos')
    foto_documento_representante = models.PhotoField('Foto do Documento do Representante', null=True, blank=True, upload_to='fotos')
    foto_procuracao = models.PhotoField('Foto da Procuração', null=True, blank=True, upload_to='fotos')

    foto_chassi_veiculo = models.PhotoField('Foto do Chassi do Veículo', null=True, blank=True, upload_to='fotos')
    foto_dianteira_veiculo = models.PhotoField('Foto Dianteira do Veículo', null=True, blank=True, upload_to='fotos')
    foto_traseira_veiculo = models.PhotoField('Foto Traseira do Veículo', null=True, blank=True, upload_to='fotos')

    foto_placa_dianteira = models.PhotoField('Foto da Placa Dianteira', null=True, blank=True, upload_to='fotos')
    foto_placa_traseira = models.PhotoField('Foto da Placa Traseira', null=True, blank=True, upload_to='fotos')
    foto_segunda_placa_traseira = models.PhotoField('Foto da Segunda Placa Traseira', null=True, blank=True, upload_to='fotos')

    foto_boletim_ocorrencia = models.PhotoField('Foto do Boletim de Ocorrência', null=True, blank=True, upload_to='fotos')
    foto_descarte_placa_dianteira = models.PhotoField('Foto do Descarte da Placa Dianteira', null=True, blank=True, upload_to='fotos')
    foto_descarte_placa_traseira = models.PhotoField('Foto do Descarte da Placa Traseira', null=True, blank=True, upload_to='fotos')
    foto_descarte_segunda_placa_traseira = models.PhotoField('Foto do Descarte da Segunda Placa Traseira', null=True, blank=True, upload_to='fotos')

    objects = ValidacaoManager()
    
    class Meta:
        icon = 'list-check'
        verbose_name = 'Validação'
        verbose_name_plural = 'Validações'
        fieldsets = {
            'Dados da Placa': ('placa', ('dianteira', 'traseira', 'segunda_traseira')),
            'Proprietário': (('cpf_proprietario', 'nome_proprietario'), 'foto_perfil_proprietario', 'foto_documento_proprietario'),
            'Representante': (('cpf_representante', 'nome_representante'), 'foto_perfil_representante', 'foto_documento_representante', 'foto_procuracao'),
            'Fotos do Veículo': ('foto_chassi_veiculo', 'foto_dianteira_veiculo', 'foto_traseira_veiculo'),
            'Fotos das Placas': ('foto_placa_dianteira', 'foto_placa_traseira', 'foto_segunda_placa_traseira'),
            'Fotos do Descarte': ('foto_boletim_ocorrencia', 'foto_descarte_placa_dianteira', 'foto_descarte_placa_traseira', 'foto_descarte_segunda_placa_traseira'),
        }

    def get_dados_placa(self):
        return self.value_set('placa', ('dianteira', 'traseira', 'segunda_traseira'))

    def get_proprietario(self):
        return self.value_set(('cpf_proprietario', 'nome_proprietario'), 'get_foto_perfil_proprietario', 'get_foto_documento_proprietario')

    def get_representante(self):
        return self.value_set(('cpf_representante', 'nome_representante'), 'get_foto_perfil_representante', 'get_foto_documento_representante', 'get_foto_procuracao')

    def get_fotos_veiculo(self):
        return self.value_set('get_foto_chassi_veiculo', 'get_foto_dianteira_veiculo', 'get_foto_traseira_veiculo')

    def get_fotos_placas(self):
        return self.value_set('get_foto_placa_dianteira', 'get_foto_placa_traseira', 'get_foto_segunda_placa_traseira')

    def get_fotos_descarte(self):
        return self.value_set('get_foto_boletim_ocorrencia', 'get_foto_descarte_placa_dianteira', 'get_foto_descarte_placa_traseira', 'get_foto_descarte_segunda_placa_traseira')

    @meta('Foto de Perfil do Proprietário', renderer='images/image')
    def get_foto_perfil_proprietario(self):
        return self.foto_perfil_proprietario

    @meta('Foto do Documento do Proprietário', renderer='images/image')
    def get_foto_documento_proprietario(self):
        return self.foto_documento_proprietario

    @meta('Foto de Perfil do Representante', renderer='images/image')
    def get_foto_perfil_representante(self):
        return self.foto_perfil_representante

    @meta('Foto do Documento do Representante', renderer='images/image')
    def get_foto_documento_representante(self):
        return self.foto_documento_representante

    @meta('Foto da Procuração', renderer='images/image')
    def get_foto_procuracao(self):
        return self.foto_procuracao

    @meta('Foto do Chassi do Veículo', renderer='images/image')
    def get_foto_chassi_veiculo(self):
        return self.foto_chassi_veiculo

    @meta('Foto Dianteira do Veículo', renderer='images/image')
    def get_foto_dianteira_veiculo(self):
        return self.foto_dianteira_veiculo

    @meta('Foto Traseira do Veículo', renderer='images/image')
    def get_foto_traseira_veiculo(self):
        return self.foto_traseira_veiculo

    @meta('Foto da Placa Dianteira', renderer='images/image')
    def get_foto_placa_dianteira(self):
        return self.foto_placa_dianteira

    @meta('Foto da Placa Traseira', renderer='images/image')
    def get_foto_placa_traseira(self):
        return self.foto_placa_traseira

    @meta('Foto da Segunda Placa Traseira', renderer='images/image')
    def get_foto_segunda_placa_traseira(self):
        return self.foto_segunda_placa_traseira

    @meta('Foto do Boletim de Ocorrência', renderer='images/image')
    def get_foto_boletim_ocorrencia(self):
        return self.foto_boletim_ocorrencia

    @meta('Foto do Descarte da Placa Dianteira', renderer='images/image')
    def get_foto_descarte_placa_dianteira(self):
        return self.foto_descarte_placa_dianteira

    @meta('Foto do Descarte da Placa Traseira', renderer='images/image')
    def get_foto_descarte_placa_traseira(self):
        return self.foto_descarte_placa_traseira

    @meta('Foto do Descarte da Segunda Placa Traseira', renderer='images/image')
    def get_foto_descarte_segunda_placa_traseira(self):
        return self.foto_descarte_segunda_placa_traseira

    def view(self):
        return self.value_set('get_dados_placa', 'get_proprietario', 'get_representante', 'get_fotos_veiculo', 'get_fotos_placas', 'get_fotos_descarte')

    def __str__(self):
        return '{}'.format(self.placa)
        
    def has_permission(self, user):
        return user.is_superuser or user.roles.contains(ADM)

