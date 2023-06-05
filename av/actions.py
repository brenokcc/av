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
