from sloth import actions
from .models import Validacao
from . import tasks
from .roles import ADM
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class QrCodeImageInput(widgets.Textarea):

    def render(self, name, value, attrs=None, **kwargs):
        attrs.update(style='display:none')
        widget = super().render(name, value, attrs=attrs, **kwargs)
        output = render_to_string('inputs/qrcode-image.html', dict(widget=widget, name=name))
        return mark_safe(output)


class CurrentLatitude(widgets.TextInput):

    def render(self, name, value, attrs=None, **kwargs):
        widget = super().render(name, value, attrs=attrs, **kwargs)
        return mark_safe(render_to_string('inputs/current-latitude.html', dict(widget=widget, name=name)))


class CurrentLongitude(widgets.TextInput):

    def render(self, name, value, attrs=None, **kwargs):
        widget = super().render(name, value, attrs=attrs, **kwargs)
        return mark_safe(render_to_string('inputs/current-longitude.html', dict(widget=widget, name=name)))


class CadastrarValidacao(actions.Action):
    class Meta:
        model = Validacao
        verbose_name = 'Cadastrar Validação'
        modal = False
        style = 'success'
        fieldsets = Validacao.metaclass().fieldsets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['latitude'].widget = CurrentLatitude()
        self.fields['longitude'].widget = CurrentLongitude()

    def submit(self):
        super().submit()
        self.redirect('/app/dashboard/{}/'.format(self.instance.pk))

    def has_permission(self, user):
        return user.roles.contains(ADM) or user.is_superuser


class EnviarFotos(actions.Action):
    class Meta:
        icon = 'camera'
        model = Validacao
        verbose_name = 'Fotos'
        modal = False
        style = 'primary'
        fieldsets = {
            'Proprietário': ('foto_perfil_proprietario', 'foto_documento_proprietario'),
            'Representante': ('foto_perfil_representante', 'foto_documento_representante', 'foto_procuracao'),
            'Fotos do Veículo': ('foto_chassi_veiculo', 'foto_dianteira_veiculo', 'foto_traseira_veiculo'),
            'Fotos das Placas': ('qrcode_placa_dianteira', 'qrcode_placa_traseira', 'qrcode_segunda_placa_traseira'),
            'Fotos do Descarte': ('foto_boletim_ocorrencia', 'foto_descarte_placa_dianteira', 'foto_descarte_placa_traseira', 'foto_descarte_segunda_placa_traseira'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ['qrcode_placa_dianteira', 'qrcode_placa_traseira', 'qrcode_segunda_placa_traseira']:
            self.fields[name].widget = QrCodeImageInput()

    def submit(self):
        super().submit()
        tasks.Validar(self.instance).start(self.request)

    def has_permission(self, user):
        return user.roles.contains(ADM) or user.is_superuser


class Validar(actions.Action):
    class Meta:
        icon = 'check2-all'
        verbose_name = 'Validar'
        modal = True
        style = 'success'

    def submit(self):
        self.instance.validar()
        super().submit()

    def has_permission(self, user):
        return user.is_superuser


class InvalidarConsulta(actions.Action):
    class Meta:
        icon = 'trash'
        verbose_name = 'Invalidar Consulta'
        modal = True
        style = 'warning'

    def submit(self):
        self.instance.valida = False
        self.instance.save()
        super().submit()

    def has_permission(self, user):
        return user.is_superuser


class CadastrarConsultaAvulso(actions.Action):
    class Meta:
        model = 'av.consultaavulso'
        verbose_name = 'Consulta Avulso'
        modal = True
        style = 'primary'
        fieldsets = {
            '': ('tipo', 'foto'),
        }

    def submit(self):
        self.save()
        self.info('RESULTADO: {}'.format(self.instance.consultar_servico()))

    def has_permission(self, user):
        return user.roles.contains(ADM) or user.is_superuser