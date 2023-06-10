from sloth import actions
from .models import Validacao
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


class CadastrarValidacao(actions.Action):
    class Meta:
        model = Validacao
        verbose_name = 'Cadastrar Validação'
        modal = False
        style = 'success'
        fieldsets = Validacao.metaclass().fieldsets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ['qrcode_placa_dianteira', 'qrcode_placa_traseira', 'qrcode_segunda_placa_traseira']:
            self.fields[name].widget = QrCodeImageInput()

    def submit(self):
        super().submit()

    def has_permission(self, user):
        return user.roles.contains(ADM) or user.is_superuser


class AlterarValidacao(actions.Action):
    class Meta:
        model = Validacao
        verbose_name = 'Realizar Alteração'
        modal = False
        style = 'primary'
        fieldsets = Validacao.metaclass().fieldsets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ['qrcode_placa_dianteira', 'qrcode_placa_traseira', 'qrcode_segunda_placa_traseira']:
            self.fields[name].widget = QrCodeImageInput()

    def submit(self):
        super().submit()

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
        return user.is_superuser # or user.roles.contains(ADM)