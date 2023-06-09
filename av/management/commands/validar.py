from django.apps import apps
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for validacao in apps.get_model('av.validacao').objects.filter(pk=1):
            validacao.validar()
