from django.core.management import BaseCommand
from av import consulta
from av import verificador


class Command(BaseCommand):
    def handle(self, *args, **options):
        from av.models import Validacao
        for validacao in Validacao.objects.filter(pk=1):
            consulta.consultar_servicos(validacao)
            for verificacao in validacao.verificacao_set.all():
                verificador.realizar_verificacoes(verificacao)
