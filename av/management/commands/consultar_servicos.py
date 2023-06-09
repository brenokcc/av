from django.core.management import BaseCommand
from av.models import Validacao
from av import consulta

class Command(BaseCommand):
    def handle(self, *args, **options):
        for validacao in Validacao.objects.filter(pk=1):
            consulta.consultar_servicos(validacao)
