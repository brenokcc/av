from sloth import actions
from .models import Validacao
from .roles import ADM



class CadastrarValidacao(actions.Action):
    class Meta:
        model = Validacao
        verbose_name = 'Cadastrar Validação'
        modal = False
        style = 'success'
        fieldsets = Validacao.metaclass().fieldsets

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