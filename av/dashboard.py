from sloth.api.dashboard import Dashboard
from .models import *


class AppDashboard(Dashboard):

    def __init__(self, request):
        super().__init__(request)
        self.styles('/static/css/sloth.css')
        self.scripts('/static/js/sloth.js', '/static/js/html5-qrcode.js')
        self.libraries(fontawesome=False, materialicons=False)
        self.web_push_notification(False)
        self.login(logo='/static/images/placa.png', title=None, mask=None, two_factor=False, actions=[])
        self.navbar(title='AV', icon='/static/images/placa.png', favicon='/static/images/br.png')
        self.header(title='AV', shadow=True)
        self.settings_menu('change_password')
        self.tools_menu('show_icons')
        self.footer(title='© 2022 Sigplac', text='Todos os direitos reservados', version='1.0.0')

        self.top_menu('av.fabricante', 'av.marca', 'av.cor', 'av.codigocor', 'av.estampador', 'av.validacao')
        self._item('links', '/app/dashboard/av/consultaavulso/add/', 'Consulta Avulso', None)

    def view(self):
        return self.objects('av.validacao').all()

