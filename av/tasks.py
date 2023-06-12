from sloth.api.tasks import Task


class Validar(Task):
    def __init__(self, validacao, *args, **kwargs):
        self.validacao = validacao
        super().__init__(*args, **kwargs)

    def run(self):
        self.validacao.validar()
        self.finalize()
