from django.apps import apps
from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--id', nargs='+', help='ID')

    def handle(self, *args, **options):
        qs = apps.get_model('av.validacao').objects.all()
        qs = qs.filter(pk__in=options['id']) if options['id'] else qs
        for validacao in qs:
            print('Validando {}'.format(validacao.pk))
            validacao.validar()
