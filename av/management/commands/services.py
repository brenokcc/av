from django.apps import apps
from django.core.management import BaseCommand
from av.services import eyedea, face_recognizer, google_lens, google_vision, liveness, plate_recognizer, vinocr


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Eyedea', eyedea.Service().test())
        print('Face Recognizer', face_recognizer.Service().test())
        print('Google Lens', google_lens.Service().test())
        print('Google Vision', google_vision.Service().test())
        print('Liveness', liveness.Service().test())
        print('Plate Recognizer', plate_recognizer.Service().test())
        print('VinOCR', vinocr.Service().test('9C6RG5020P0054000'))
