from datetime import datetime
import geopy.distance
from sloth.db import models, role, meta
from .roles import ADM
from django.conf import settings


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


class EstampadorManager(models.Manager):
    def all(self):
        return self

 
class Estampador(models.Model):
    cnpj = models.BrCnpjField('CNPJ')
    
    objects = EstampadorManager()
    
    class Meta:
        verbose_name = 'Estampador'
        verbose_name_plural = 'Estampadores'

    def get_dados_gerais(self):
        return self.value_set('cnpj')

    def get_operadores(self):
        return self.operador_set.related_field('estampador').display('get_foto', 'cpf')

    @meta('Locais de Instalação')
    def get_locais_instalacao(self):
        return self.localinstalacao_set.related_field('estampador').display('latitude', 'longitude', 'get_geolocalizacao').rows()

    def view(self):
        return self.value_set('get_dados_gerais', 'get_operadores', 'get_locais_instalacao')
        
    def __str__(self):
        return self.cnpj
        
    def has_permission(self, user):
        return user.is_superuser or user.roles.contains(ADM)



class OperadorManager(models.Manager):
    def all(self):
        return self


class Operador(models.Model):
    estampador = models.ForeignKey(Estampador, verbose_name='Estampador')
    cpf = models.BrCpfField('CPF')
    foto = models.PhotoField('Foto', upload_to='fotos')

    objects = OperadorManager()

    class Meta:
        verbose_name = 'Operador'
        verbose_name_plural = 'Operadores'

    def __str__(self):
        return self.cpf

    @meta('Foto', renderer='images/image')
    def get_foto(self):
        return self.foto

    def get_url_foto(self):
        return '{}/media/{}'.format(settings.SITE_URL, self.foto.name) if self.foto else None

    def has_permission(self, user):
        return user.is_superuser or user.roles.contains(ADM)


class LocalInstalacaoManager(models.Manager):
    def all(self):
        return self

 
class LocalInstalacao(models.Model):
    estampador = models.ForeignKey(Estampador, verbose_name='Estampador')
    nome = models.CharField('Nome')
    latitude = models.CharField('Latitude')
    longitude = models.CharField('Longitude')
    
    objects = LocalInstalacaoManager()
    
    class Meta:
        verbose_name = 'Local de Instalação'
        verbose_name_plural = 'Locais de Instalação'
        
    def __str__(self):
        return self.nome
        
    def has_permission(self, user):
        return user.is_superuser or user.roles.contains(ADM)

    @meta('Geolocalização', renderer='maps/geolocation')
    def get_geolocalizacao(self):
        return self.latitude, self.longitude

    def calcular_distancia(self, latitude, longitude):
        coords_1 = (self.latitude, self.longitude)
        coords_2 = (latitude, longitude)
        distancia = geopy.distance.geodesic(coords_1, coords_2)
        return int(distancia.m)


class FabricanteManager(models.Manager):
    def all(self):
        return self.lookups(ADM)


class Fabricante(models.Model):
    nome = models.CharField('Nome')

    objects = FabricanteManager()

    class Meta:
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Fabricante'

    def __str__(self):
        return self.nome

    def has_permission(self, user):
        return user.is_superuser or user.roles.contains(ADM)


class MarcaManager(models.Manager):
    def all(self):
        return self.lookups(ADM).search('nome', 'fabricante__nome')


class Marca(models.Model):
    nome = models.CharField('None')
    fabricante = models.ForeignKey(Fabricante, verbose_name='Fabricante')

    objects = MarcaManager()

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return '{} ({})'.format(self.nome, self.fabricante)

    def has_permission(self, user):
        return user.is_superuser or user.roles.contains(ADM)


class CorManager(models.Manager):
    def all(self):
        return self.lookups(ADM)


class Cor(models.Model):
    nome = models.CharField('Nome')

    objects = CorManager()

    class Meta:
        verbose_name = 'Cor'
        verbose_name_plural = 'Cores'

    def __str__(self):
        return self.nome

    def has_permission(self, user):
        return user.is_superuser or user.roles.contains(ADM)


class CodigoCorManager(models.Manager):
    def all(self):
        return self.display('nome', 'cores')


class CodigoCor(models.Model):
    nome = models.CharField('Nome')
    cores = models.ManyToManyField('av.Cor', verbose_name='Cores', blank=True)

    objects = CodigoCorManager()

    class Meta:
        verbose_name = 'Código de Cor'
        verbose_name_plural = 'Códigos de Cores'

    def __str__(self):
        return '{}'.format(self.pk)

    def has_permission(self, user):
        return user.is_superuser



class ValidacaoManager(models.Manager):
    def all(self):
        return self.lookups(ADM).display('placa', 'chassi', 'marca', 'cor', 'estampador', 'operador', 'cpf_proprietario', 'nome_proprietario')

 
class Validacao(models.Model):
    placa = models.BrCarPlateField('Número da Placa')
    chassi = models.CharField('Chassi', null=True)
    marca = models.ForeignKey(Marca, verbose_name='Marca', null=True)
    cor = models.ForeignKey(Cor, verbose_name='Cor', null=True)

    estampador = models.ForeignKey(Estampador, verbose_name='Estampador', null=True)
    operador = models.ForeignKey(Operador, verbose_name='Operador', null=True)
    foto_perfil_operador = models.PhotoField(verbose_name='Foto de Perfil do Operador', null=True)
    latitude = models.CharField('Latitude', null=True)
    longitude = models.CharField('Longitude', null=True)

    cpf_proprietario = models.BrCpfField('CPF do Proprietário')
    nome_proprietario = models.CharField('Nome do Proprietário')
    foto_perfil_proprietario = models.PhotoField('Foto de Perfil do Proprietário', null=True, blank=True, upload_to='fotos', max_width=500)
    foto_documento_proprietario = models.PhotoField('Foto do Documento do Proprietário', null=True, blank=True, upload_to='fotos', max_width=800)

    cpf_representante = models.BrCpfField('CPF do Representante', null=True, blank=True)
    nome_representante = models.CharField('Nome do Representante', null=True, blank=True)
    foto_perfil_representante = models.PhotoField('Foto de Perfil do Representante', null=True, blank=True, upload_to='fotos', max_width=500)
    foto_documento_representante = models.PhotoField('Foto do Documento do Representante', null=True, blank=True, upload_to='fotos', max_width=800)
    foto_procuracao = models.PhotoField('Foto da Procuração', null=True, blank=True, upload_to='fotos', max_width=800)

    foto_chassi_veiculo = models.PhotoField('Foto do Chassi do Veículo', null=True, blank=True, upload_to='fotos', max_width=800)
    foto_dianteira_veiculo = models.PhotoField('Foto Dianteira do Veículo', null=True, blank=True, upload_to='fotos', max_width=500)
    foto_traseira_veiculo = models.PhotoField('Foto Traseira do Veículo', null=True, blank=True, upload_to='fotos', max_width=500)

    foto_placa_dianteira = models.PhotoField('Foto da Placa Dianteira', null=True, blank=True, upload_to='fotos', max_width=500)
    foto_placa_traseira = models.PhotoField('Foto da Placa Traseira', null=True, blank=True, upload_to='fotos', max_width=500)
    foto_segunda_placa_traseira = models.PhotoField('Foto da Segunda Placa Traseira', null=True, blank=True, upload_to='fotos', max_width=500)

    foto_boletim_ocorrencia = models.PhotoField('Foto do Boletim de Ocorrência', null=True, blank=True, upload_to='fotos', max_width=800)
    foto_descarte_placa_dianteira = models.PhotoField('Foto do Descarte da Placa Dianteira', null=True, blank=True, upload_to='fotos', max_width=500)
    foto_descarte_placa_traseira = models.PhotoField('Foto do Descarte da Placa Traseira', null=True, blank=True, upload_to='fotos', max_width=500)
    foto_descarte_segunda_placa_traseira = models.PhotoField('Foto do Descarte da Segunda Placa Traseira', null=True, blank=True, upload_to='fotos', max_width=500)

    objects = ValidacaoManager()
    
    class Meta:
        icon = 'list-check'
        verbose_name = 'Validação'
        verbose_name_plural = 'Validações'
        fieldsets = {
            'Dados Gerais': ('estampador', ('placa', 'chassi'), ('marca', 'cor')),
            'Operador': (('operador', 'foto_perfil_operador'),),
            'Localização': (('latitude', 'longitude'),),
            'Proprietário': (('cpf_proprietario', 'nome_proprietario'), 'foto_perfil_proprietario', 'foto_documento_proprietario'),
            'Representante': (('cpf_representante', 'nome_representante'), 'foto_perfil_representante', 'foto_documento_representante', 'foto_procuracao'),
            'Fotos do Veículo': ('foto_chassi_veiculo', 'foto_dianteira_veiculo', 'foto_traseira_veiculo'),
            'Fotos das Placas': ('foto_placa_dianteira', 'foto_placa_traseira', 'foto_segunda_placa_traseira'),
            'Fotos do Descarte': ('foto_boletim_ocorrencia', 'foto_descarte_placa_dianteira', 'foto_descarte_placa_traseira', 'foto_descarte_segunda_placa_traseira'),
        }

    def get_dados_gerais(self):
        return self.value_set('estampador', ('placa', 'chassi'), ('marca', 'cor'))

    @meta('Dados do Operador')
    def get_operador(self):
        return self.value_set('operador', 'get_foto_perfil_operador')

    @meta('Foto do Operador', renderer='images/image')
    def get_foto_perfil_operador(self):
        return self.foto_perfil_operador

    @meta('Localização')
    def get_localizacao(self):
        return self.value_set(('latitude', 'longitude'))


    @meta('Dados do Proprietário')
    def get_proprietario(self):
        return self.value_set(('cpf_proprietario', 'nome_proprietario'), 'get_foto_perfil_proprietario', 'get_foto_documento_proprietario')

    @meta('Dados do Representante')
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

    @meta('Consultas')
    def get_consultas(self):
        return self.consulta_set.display('tipo', 'data_hora', 'get_valor', 'get_valida').actions('view')

    @meta('Verificações')
    def get_verificacoes(self):
        return self.verificacao_set.display('descricao', 'get_satisfeita', 'observacao')

    def view(self):
        # self.consultar()
        return self.value_set('get_dados_gerais', 'get_localizacao', 'get_operador', 'get_proprietario', 'get_representante', 'get_fotos_veiculo', 'get_fotos_placas', 'get_fotos_descarte', 'get_consultas', 'get_verificacoes').actions('validar', 'alterar_validacao')

    def __str__(self):
        return '{}'.format(self.placa)
        
    def has_permission(self, user):
        return user.is_superuser or user.roles.contains(ADM)

    def get_url(self, attr_name):
        foto = getattr(self, attr_name)
        return '{}/media/{}'.format(settings.SITE_URL, foto.name) if foto else None

    def gerar_verificacoes(self):
        tipos = [
            Verificacao.GEOLOCALIZACAO,
            Verificacao.RECONHECIMENTO_OPERADOR,
            Verificacao.PRESENCA_OPERADOR,
            Verificacao.NOME_PROPRIETARIO,
            Verificacao.CPF_PROPRIETARIO,
            Verificacao.RECONHECIMENTO_PROPRIETARIO,
            Verificacao.PRESENCA_PROPRIETARIO,
            Verificacao.NUMERO_CHASSI,
            Verificacao.CARACTERISTICA_CHASSI,
            Verificacao.MARCA_VEICULO,
            Verificacao.COR_VEICULO
        ]
        if self.nome_representante:
            tipos.extend([
                Verificacao.NOME_REPRESENTANTE,
                Verificacao.CPF_REPRESENTANTE,
                Verificacao.RECONHECIMENTO_REPRESENTANTE,
                Verificacao.PRESENCA_REPRESENTANTE,
                Verificacao.TITULO_PROCURACAO,
                Verificacao.DADOS_PROPRIETARIO_PROCURACAO,
                Verificacao.DADOS_REPRESENTANTE_PROCURACAO,
                Verificacao.PLACA_PROCURACAO,
                Verificacao.ASSINATURA_PROCURACAO
            ])
        if self.foto_placa_dianteira:
            tipos.extend([
                Verificacao.NUMERO_PLACA_DIANTEIRA,
                Verificacao.ITENS_SEGURANCA_PLACA_DIANTEIRA,
                Verificacao.QRCODE_PLACA_DIANTEIRA
            ])
        if self.foto_placa_traseira:
            tipos.extend([
                Verificacao.NUMERO_PLACA_TRASEIRA,
                Verificacao.ITENS_SEGURANCA_PLACA_TRASEIRA,
                Verificacao.QRCODE_PLACA_TRASEIRA
            ])
        if self.foto_segunda_placa_traseira:
            tipos.extend([
                Verificacao.NUMERO_SEGUNDA_PLACA_TRASEIRA,
                Verificacao.ITENS_SEGUNDA_SEGURANCA_PLACA_TRASEIRA,
                Verificacao.QRCODE_SEGUNDA_PLACA_TRASEIRA
            ])
        if self.foto_boletim_ocorrencia:
            tipos.extend([
                Verificacao.TITULO_BOLETIM_OCORRENCIA,
                Verificacao.DADOS_PROPRIETARIO_BOLETIM_OCORRENCIA,
                Verificacao.PLACA_BOLETIM_OCORRENCIA
            ])
        if self.foto_descarte_placa_dianteira:
            tipos.append(Verificacao.DESCARTE_PLACA_DIANTEIRA)
        if self.foto_descarte_placa_traseira:
            tipos.append(Verificacao.DESCARTE_PLACA_TRASEIRA)
        if self.get_foto_descarte_segunda_placa_traseira:
            tipos.append(Verificacao.DESCARTE_SEGUNDA_PLACA_TRASEIRA)
        for tipo in tipos:
            Verificacao.objects.get_or_create(validacao=self, descricao=tipo, defaults=dict(satisfeita=None))

    def validar(self):
        from . import consultor
        from . import verificador
        consultor.consultar_servicos(self)
        for verificacao in self.verificacao_set.all():
            verificador.realizar_verificacoes(verificacao)


class ConsultaManager(models.Manager):
    def all(self):
        return self

 
class Consulta(models.Model):
    FOTO_OPERADOR = 'Foto do Operador'
    PRESENCA_OPERADOR = 'Presença do Operador'
    DOCUMENTO_PROPRIETARIO = 'Documento do Proprietário'
    DOCUMENTO_REPRESENTANTE = 'Documento do Representante'
    MARCA_FOTO_DIANTEIRA = 'Marca da Foto Dianteira'
    MARCA_FOTO_TRASEIRA = 'Marca da Foto Traseira'
    FOTO_PROPRIETARIO = 'Foto do Proprietário'
    PRESENCA_PROPRIETARIO = 'Presença do Proprietário'
    FOTO_REPRESENTANTE = 'Foto do Representante'
    PRESENCA_REPRESENTANTE = 'Presença do Representante'
    FOTO_PLACA_DIANTEIRA = 'Foto da Placa Dianteira'
    FOTO_PLACA_TRASEIRA = 'Foto da Placa Traseira'
    FOTO_SEGUNDA_PLACA_TRASEIRA = 'Foto da Segunda Placa Traseira'
    OCR_PLACA_DIANTEIRA = 'OCR da Placa Dianteira'
    OCR_PLACA_TRASEIRA = 'OCR da Placa Traseira'
    OCR_SEGUNDA_PLACA_TRASEIRA = 'OCR da Segunda Placa Traseira'
    NUMERO_CHASSI = 'Número do Chassi'
    CARACTERISTICAS_CHASSI = 'Características do Chassi'
    COR_VEICULO = 'Cor do Veículo'

    validacao = models.ForeignKey(Validacao, verbose_name='Validação')
    tipo = models.CharField('Tipo')
    data_hora = models.DateTimeField('Data/Hora')
    url = models.CharField('URL', null=True, blank=True)
    valor = models.TextField('Valor')
    valida = models.BooleanField('Válida', default=True)
    
    objects = ConsultaManager()
    
    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        fieldsets = {
            'Dados Gerais': ('validacao', 'valor', 'valida'),
        }
        
    def __str__(self):
        return '{}'.format(self.pk)

    def get_valor(self):
        valor = self.valor
        if valor and len(valor) > 100:
            valor = '{}...'.format(valor[0:100])
        return valor

    @meta('Válida', renderer='badges/boolean')
    def get_valida(self):
        return self.valida
        
    def has_permission(self, user):
        return user.is_superuser


class VerificacaoManager(models.Manager):
    def all(self):
        return self

 
class Verificacao(models.Model):
    GEOLOCALIZACAO = 'Geolocalização de instalação previamente cadastrada'
    RECONHECIMENTO_OPERADOR = 'Compatibilidade entre a foto de perfil do operador com a foto previamente cadastrada'
    PRESENCA_OPERADOR = 'Foto do operador retirada no momento do emplacamento'

    NOME_PROPRIETARIO = 'Nome do proprietário presente no documento de identificação'
    CPF_PROPRIETARIO = 'CPF do proprietário presente no documento de identificação'
    RECONHECIMENTO_PROPRIETARIO = 'Compatibilidade entre a foto de perfil e a do documento do proprietário'
    PRESENCA_PROPRIETARIO = 'Foto do proprietário retirada no momento do emplacamento'

    NOME_REPRESENTANTE = 'Nome do representante presente no documento de identificação'
    CPF_REPRESENTANTE = 'CPF do representante presente no documento de identificação'
    RECONHECIMENTO_REPRESENTANTE = 'Compatibilidade entre a foto de perfil e a do documento do representante'
    PRESENCA_REPRESENTANTE = 'Foto do representante retirada no momento do emplacamento'

    TITULO_PROCURACAO = 'Palavra "procuração" presente no documento da procuração'
    DADOS_PROPRIETARIO_PROCURACAO = 'Nome e CPF do proprietário presente no documento da procuração'
    DADOS_REPRESENTANTE_PROCURACAO = 'Nome e CPF do representante presente no documento da procuração'
    PLACA_PROCURACAO = 'Número da placa presente no documento da procuração'
    ASSINATURA_PROCURACAO = 'Assinatura presente no documento da procuração'

    NUMERO_CHASSI = 'Número do chassi do veículo'
    CARACTERISTICA_CHASSI = 'Característica do chassi do veículo'

    MARCA_VEICULO = 'Marca do veículo'
    COR_VEICULO = 'Cor do veículo'

    NUMERO_PLACA_DIANTEIRA = 'Número da placa dianteira'
    ITENS_SEGURANCA_PLACA_DIANTEIRA = 'Itens de segurança da placa dianteira'
    QRCODE_PLACA_DIANTEIRA = 'QrCode da placa dianteira'

    NUMERO_PLACA_TRASEIRA = 'Número da placa traseira'
    ITENS_SEGURANCA_PLACA_TRASEIRA = 'Itens de segurança da placa traseira'
    QRCODE_PLACA_TRASEIRA = 'QrCode da placa traseira'

    NUMERO_SEGUNDA_PLACA_TRASEIRA = 'Número da segunda placa traseira'
    ITENS_SEGUNDA_SEGURANCA_PLACA_TRASEIRA = 'Itens de segurança segunda da placa traseira'
    QRCODE_SEGUNDA_PLACA_TRASEIRA = 'QrCode da segunda placa traseira'

    TITULO_BOLETIM_OCORRENCIA = 'Palavra "BOLETIM DE OCORRÊNCIA" presente no documento do boletim de ocorrência'
    DADOS_PROPRIETARIO_BOLETIM_OCORRENCIA = 'Nome e CPF do representante presente no documento do boletim de ocorrência'
    PLACA_BOLETIM_OCORRENCIA = 'Número da placa presente no documento do boletim de ocorrência'

    DESCARTE_PLACA_DIANTEIRA = 'Corte na placa dianteira descartada'
    DESCARTE_PLACA_TRASEIRA = 'Corte na placa traseira descartada'
    DESCARTE_SEGUNDA_PLACA_TRASEIRA = 'Corte na segunda placa traseira descartada'

    validacao = models.ForeignKey(Validacao, verbose_name='Validação')
    descricao = models.CharField('Descrição')
    satisfeita = models.BooleanField('Satisfeita', null=True)
    observacao = models.CharField('Observação', null=True)

    objects = VerificacaoManager()
    
    class Meta:
        verbose_name = 'Verificação'
        verbose_name_plural = 'Verificações'
        
    def __str__(self):
        return '{}'.format(self.pk)
        
    def has_permission(self, user):
        return user.is_superuser

    @meta('Satisfeita', renderer='badges/boolean')
    def get_satisfeita(self):
        return self.satisfeita
