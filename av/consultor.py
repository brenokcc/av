import json
from datetime import datetime
from .services import google_vision, google_lens, face_recognizer, liveness, plate_recognizer, eyedea
from .models import Consulta, Validacao

def consultar_foto_operador(validacao):
    url1 = validacao.get_url('foto_perfil_operador')
    url2 = validacao.operador.get_url_foto()
    if url1 and url2 and not validacao.consulta_set.filter(tipo=Consulta.FOTO_OPERADOR, valida=True).exists():
        print('Verificando foto do operador...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url1)
        consulta.tipo = Consulta.FOTO_OPERADOR
        consulta.valor = face_recognizer.Service().match(url1, url2)
        consulta.save()

def consultar_presenca_operador(validacao):
    url = validacao.get_url('foto_perfil_operador')
    if url and not validacao.consulta_set.filter(tipo=Consulta.PRESENCA_OPERADOR, valida=True).exists():
        print('Verificando a presença do operador...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.PRESENCA_OPERADOR
        consulta.valor = liveness.Service().verify(url)
        consulta.save()

def consultar_documento_proprietario(validacao):
    url = validacao.get_url('foto_documento_proprietario')
    if url and not validacao.consulta_set.filter(tipo=Consulta.DOCUMENTO_PROPRIETARIO, valida=True).exists():
        print('Verificando documento do proprietário...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.DOCUMENTO_PROPRIETARIO
        consulta.valor = google_vision.Service().detect_text(url)
        consulta.save()

def consultar_foto_proprietario(validacao):
    url1 = validacao.get_url('foto_perfil_proprietario')
    url2 = validacao.get_url('foto_documento_proprietario')
    if url1 and url2 and not validacao.consulta_set.filter(tipo=Consulta.FOTO_PROPRIETARIO, valida=True).exists():
        print('Verificando foto do proprietário...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.FOTO_PROPRIETARIO
        consulta.valor = face_recognizer.Service().match(url1, url2)
        consulta.save()

def consultar_presenca_proprietario(validacao):
    url = validacao.get_url('foto_perfil_proprietario')
    if url and not validacao.consulta_set.filter(tipo=Consulta.PRESENCA_PROPRIETARIO, valida=True).exists():
        print('Verificando a presença do proprietário...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.PRESENCA_PROPRIETARIO
        consulta.valor = liveness.Service().verify(url)
        consulta.save()

def consultar_documento_representante(validacao):
    url = validacao.get_url('foto_documento_representante')
    if url and not validacao.consulta_set.filter(tipo=Consulta.DOCUMENTO_REPRESENTANTE, valida=True).exists():
        print('Verificando documento do representante...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.DOCUMENTO_REPRESENTANTE
        consulta.valor = google_vision.Service().detect_text(url)
        consulta.save()

def consultar_foto_representante(validacao):
    url1 = validacao.get_url('foto_perfil_representante')
    url2 = validacao.get_url('foto_documento_representante')
    if url1 and url2 and not validacao.consulta_set.filter(tipo=Consulta.FOTO_REPRESENTANTE, valida=True).exists():
        print('Verificando foto do representante...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.FOTO_REPRESENTANTE
        consulta.valor = face_recognizer.Service().match(url1, url2)
        consulta.save()

def consultar_marca_foto_dianteira(validacao):
    url = validacao.get_url('foto_dianteira_veiculo')
    if url and not validacao.consulta_set.filter(tipo=Consulta.MARCA_FOTO_DIANTEIRA, valida=True).exists():
        print('Verificando foto dianteira do veículo...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.MARCA_FOTO_DIANTEIRA
        consulta.valor = google_lens.Service().detect_brand(url)
        consulta.save()

def consultar_marca_foto_traseira(validacao):
    url = validacao.get_url('foto_traseira_veiculo')
    if url and not validacao.consulta_set.filter(tipo=Consulta.MARCA_FOTO_TRASEIRA, valida=True).exists():
        print('Verificando foto traseira do veículo...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.MARCA_FOTO_TRASEIRA
        consulta.valor = google_lens.Service().detect_brand(url)
        consulta.save()

def consultar_foto_placa_dianteira(validacao):
    url = validacao.get_url('foto_placa_dianteira')
    if url and not validacao.consulta_set.filter(tipo=Consulta.FOTO_PLACA_DIANTEIRA, valida=True).exists():
        print('Verificando foto da placa dianteira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.FOTO_PLACA_DIANTEIRA
        consulta.valor = plate_recognizer.Service().detect_plate(url)
        consulta.save()

def consultar_foto_placa_traseira(validacao):
    url = validacao.get_url('foto_placa_traseira')
    if url and not validacao.consulta_set.filter(tipo=Consulta.FOTO_PLACA_TRASEIRA, valida=True).exists():
        print('Verificando foto da placa traseira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.FOTO_PLACA_TRASEIRA
        consulta.valor = google_vision.Service().detect_text(url)
        consulta.save()

def consultar_foto_segunda_placa_traseira(validacao):
    url = validacao.get_url('foto_segunda_placa_traseira')
    if url and not validacao.consulta_set.filter(tipo=Consulta.FOTO_SEGUNDA_PLACA_TRASEIRA, valida=True).exists():
        print('Verificando foto da segunda placa traseira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.FOTO_SEGUNDA_PLACA_TRASEIRA
        consulta.valor = google_vision.Service().detect_text(url)
        consulta.save()

def consultar_ocr_placa_dianteira(validacao):
    url = validacao.get_url('foto_placa_dianteira')
    if url and not validacao.consulta_set.filter(tipo=Consulta.OCR_PLACA_DIANTEIRA, valida=True).exists():
        print('Verificando OCR da foto da placa dianteira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.OCR_PLACA_DIANTEIRA
        consulta.valor = google_vision.Service().detect_text(url)
        consulta.save()

def consultar_ocr_placa_traseira(validacao):
    url = validacao.get_url('foto_placa_traseira')
    if url and not validacao.consulta_set.filter(tipo=Consulta.OCR_PLACA_TRASEIRA, valida=True).exists():
        print('Verificando OCR da foto da placa traseira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.OCR_PLACA_TRASEIRA
        consulta.valor = google_vision.Service().detect_text(url)
        consulta.save()

def consultar_ocr_segunda_placa_traseira(validacao):
    url = validacao.get_url('foto_segunda_placa_traseira')
    if url and not validacao.consulta_set.filter(tipo=Consulta.OCR_SEGUNDA_PLACA_TRASEIRA, valida=True).exists():
        print('Verificando OCR da foto da segunda placa traseira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.OCR_SEGUNDA_PLACA_TRASEIRA
        consulta.valor = google_vision.Service().detect_text(url)
        consulta.save()

def consultar_numero_chassi(validacao):
    url = validacao.get_url('foto_chassi_veiculo')
    if url and not validacao.consulta_set.filter(tipo=Consulta.NUMERO_CHASSI, valida=True).exists():
        print('Verificando número do chassi...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.NUMERO_CHASSI
        consulta.valor = google_vision.Service().detect_text(url)
        consulta.save()

def consultar_caracteristicas_chassi(validacao):
    url = validacao.get_url('foto_chassi_veiculo')
    if url and not validacao.consulta_set.filter(tipo=Consulta.CARACTERISTICAS_CHASSI, valida=True).exists():
        print('Verificando características do chassi...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.CARACTERISTICAS_CHASSI
        consulta.valor = json.dumps(google_vision.Service().detect_labels(url)).upper()
        consulta.save()

def consultar_cor_veiculo(validacao):
    url = validacao.get_url('foto_dianteira_veiculo')
    if url and not validacao.consulta_set.filter(tipo=Consulta.COR_VEICULO, valida=True).exists():
        print('Verificando cor do veículo...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.COR_VEICULO
        consulta.valor = eyedea.Service().detect_color(url)
        consulta.save()

def consultar_servicos(validacao):
    consultar_foto_operador(validacao)
    consultar_presenca_operador(validacao)
    consultar_documento_proprietario(validacao)
    consultar_foto_proprietario(validacao)
    consultar_documento_representante(validacao)
    consultar_foto_representante(validacao)
    consultar_marca_foto_dianteira(validacao)
    consultar_marca_foto_traseira(validacao)
    consultar_foto_placa_dianteira(validacao)
    consultar_foto_placa_traseira(validacao)
    consultar_foto_segunda_placa_traseira(validacao)
    consultar_ocr_placa_dianteira(validacao)
    consultar_ocr_placa_traseira(validacao)
    consultar_ocr_segunda_placa_traseira(validacao)
    consultar_numero_chassi(validacao)
    consultar_caracteristicas_chassi(validacao)
    consultar_presenca_proprietario(validacao)
    consultar_cor_veiculo(validacao)