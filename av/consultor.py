import json
from datetime import datetime
from .services import google_vision, google_lens, face_recognizer, liveness, plate_recognizer, eyedea, vinocr
from .models import Consulta, Validacao

FAKE = False

def consultar_foto_operador(validacao):
    url1 = validacao.get_url('foto_perfil_operador')
    url2 = validacao.operador.get_url_foto()
    qs = validacao.consulta_set.filter(tipo=Consulta.FOTO_OPERADOR, valida=True)
    if url1 and url2 and not qs.filter(url=url1).exists():
        qs.update(valida=False)
        print('Verificando foto do operador...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url1)
        consulta.tipo = Consulta.FOTO_OPERADOR
        consulta.valor = '{}' if FAKE else 'MATCH' or face_recognizer.Service().match(url1, url2)
        consulta.save()

def consultar_presenca_operador(validacao):
    url = validacao.get_url('foto_perfil_operador')
    qs = validacao.consulta_set.filter(tipo=Consulta.PRESENCA_OPERADOR, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando a presença do operador...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.PRESENCA_OPERADOR
        consulta.valor = '{}' if FAKE else liveness.Service().verify(url)
        consulta.save()

def consultar_documento_proprietario(validacao):
    url = validacao.get_url('foto_documento_proprietario')
    qs = validacao.consulta_set.filter(tipo=Consulta.DOCUMENTO_PROPRIETARIO, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando documento do proprietário...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.DOCUMENTO_PROPRIETARIO
        consulta.valor = '{}' if FAKE else google_vision.Service().detect_text(url)
        consulta.save()

def consultar_foto_proprietario(validacao):
    url1 = validacao.get_url('foto_perfil_proprietario')
    url2 = validacao.get_url('foto_documento_proprietario')
    qs = validacao.consulta_set.filter(tipo=Consulta.FOTO_PROPRIETARIO, valida=True)
    if url1 and url2 and not qs.filter(url=url1).exists():
        qs.update(valida=False)
        print('Verificando foto do proprietário...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url1)
        consulta.tipo = Consulta.FOTO_PROPRIETARIO
        consulta.valor = '{}' if FAKE else face_recognizer.Service().match(url1, url2)
        consulta.save()

def consultar_presenca_proprietario(validacao):
    url = validacao.get_url('foto_perfil_proprietario')
    qs = validacao.consulta_set.filter(tipo=Consulta.PRESENCA_PROPRIETARIO, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando a presença do proprietário...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.PRESENCA_PROPRIETARIO
        consulta.valor = '{}' if FAKE else liveness.Service().verify(url)
        consulta.save()

def consultar_documento_representante(validacao):
    url = validacao.get_url('foto_documento_representante')
    qs = validacao.consulta_set.filter(tipo=Consulta.DOCUMENTO_REPRESENTANTE, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando documento do representante...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.DOCUMENTO_REPRESENTANTE
        consulta.valor = '{}' if FAKE else google_vision.Service().detect_text(url)
        consulta.save()

def consultar_foto_representante(validacao):
    url1 = validacao.get_url('foto_perfil_representante')
    url2 = validacao.get_url('foto_documento_representante')
    qs = validacao.consulta_set.filter(tipo=Consulta.FOTO_REPRESENTANTE, valida=True)
    if url1 and url2 and not qs.filter(url=url1).exists():
        qs.update(valida=False)
        print('Verificando foto do representante...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url1)
        consulta.tipo = Consulta.FOTO_REPRESENTANTE
        consulta.valor = '{}' if FAKE else face_recognizer.Service().match(url1, url2)
        consulta.save()

def consultar_marca_foto_dianteira(validacao):
    url = validacao.get_url('foto_dianteira_veiculo')
    qs = validacao.consulta_set.filter(tipo=Consulta.MARCA_FOTO_DIANTEIRA, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando foto dianteira do veículo...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.MARCA_FOTO_DIANTEIRA
        consulta.valor = '{}' if FAKE else google_lens.Service().detect_brand(url)
        consulta.save()

def consultar_marca_foto_traseira(validacao):
    url = validacao.get_url('foto_traseira_veiculo')
    qs = validacao.consulta_set.filter(tipo=Consulta.MARCA_FOTO_TRASEIRA, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando foto traseira do veículo...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.MARCA_FOTO_TRASEIRA
        consulta.valor = '{}' if FAKE else google_lens.Service().detect_brand(url)
        consulta.save()

def consultar_foto_placa_dianteira(validacao):
    url = validacao.get_url('foto_placa_dianteira')
    qs = validacao.consulta_set.filter(tipo=Consulta.FOTO_PLACA_DIANTEIRA, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando foto da placa dianteira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.FOTO_PLACA_DIANTEIRA
        consulta.valor = '{}' if FAKE else plate_recognizer.Service().detect_plate(url)
        consulta.save()

def consultar_foto_placa_traseira(validacao):
    url = validacao.get_url('foto_placa_traseira')
    qs = validacao.consulta_set.filter(tipo=Consulta.FOTO_PLACA_TRASEIRA, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando foto da placa traseira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.FOTO_PLACA_TRASEIRA
        consulta.valor = '{}' if FAKE else google_vision.Service().detect_text(url)
        consulta.save()

def consultar_foto_segunda_placa_traseira(validacao):
    url = validacao.get_url('foto_segunda_placa_traseira')
    qs = validacao.consulta_set.filter(tipo=Consulta.FOTO_SEGUNDA_PLACA_TRASEIRA, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando foto da segunda placa traseira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.FOTO_SEGUNDA_PLACA_TRASEIRA
        consulta.valor = '{}' if FAKE else google_vision.Service().detect_text(url)
        consulta.save()

def consultar_ocr_placa_dianteira(validacao):
    url = validacao.get_url('foto_placa_dianteira')
    qs = validacao.consulta_set.filter(tipo=Consulta.OCR_PLACA_DIANTEIRA, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando OCR da foto da placa dianteira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.OCR_PLACA_DIANTEIRA
        consulta.valor = '{}' if FAKE else google_vision.Service().detect_text(url)
        consulta.save()

def consultar_ocr_placa_traseira(validacao):
    url = validacao.get_url('foto_placa_traseira')
    qs = validacao.consulta_set.filter(tipo=Consulta.OCR_PLACA_TRASEIRA, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando OCR da foto da placa traseira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.OCR_PLACA_TRASEIRA
        consulta.valor = '{}' if FAKE else google_vision.Service().detect_text(url)
        consulta.save()

def consultar_ocr_segunda_placa_traseira(validacao):
    url = validacao.get_url('foto_segunda_placa_traseira')
    qs = validacao.consulta_set.filter(tipo=Consulta.OCR_SEGUNDA_PLACA_TRASEIRA, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando OCR da foto da segunda placa traseira...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.OCR_SEGUNDA_PLACA_TRASEIRA
        consulta.valor = '{}' if FAKE else google_vision.Service().detect_text(url)
        consulta.save()

def consultar_numero_chassi(validacao):
    url = validacao.get_url('foto_chassi_veiculo')
    qs = validacao.consulta_set.filter(tipo=Consulta.NUMERO_CHASSI, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando número do chassi...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.NUMERO_CHASSI
        consulta.valor = '{}' if FAKE else vinocr.Service().detect_vin(url)
        consulta.save()

def consultar_numero_chassi2(validacao):
    url = validacao.get_url('foto_chassi_veiculo')
    qs = validacao.consulta_set.filter(tipo=Consulta.NUMERO_CHASSI_2, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando número do chassi...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.NUMERO_CHASSI_2
        consulta.valor = '{}' if FAKE else google_vision.Service().detect_text(url)
        consulta.save()

def consultar_caracteristicas_chassi(validacao):
    url = validacao.get_url('foto_chassi_veiculo')
    qs = validacao.consulta_set.filter(tipo=Consulta.CARACTERISTICAS_CHASSI, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando características do chassi...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.CARACTERISTICAS_CHASSI
        consulta.valor = '{}' if FAKE else json.dumps(google_vision.Service().detect_labels(url)).upper()
        consulta.save()

def consultar_cor_veiculo(validacao):
    url = validacao.get_url('foto_dianteira_veiculo')
    qs = validacao.consulta_set.filter(tipo=Consulta.COR_VEICULO, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando cor do veículo...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.COR_VEICULO
        consulta.valor = '{}' if FAKE else eyedea.Service().detect_color(url)
        consulta.save()


def consultar_procuracao(validacao):
    url = validacao.get_url('foto_procuracao')
    qs = validacao.consulta_set.filter(tipo=Consulta.PROCURACAO, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando procuração...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.PROCURACAO
        consulta.valor = '{}' if FAKE else google_vision.Service().detect_text(url)
        consulta.save()


def consultar_boletim_ocorrencia(validacao):
    url = validacao.get_url('foto_boletim_ocorrencia')
    qs = validacao.consulta_set.filter(tipo=Consulta.BOLETIM_OCORRENCIA, valida=True)
    if url and not qs.filter(url=url).exists():
        qs.update(valida=False)
        print('Verificando boletim de ocorrência...')
        consulta = Consulta(validacao=validacao, data_hora=datetime.now(), url=url)
        consulta.tipo = Consulta.BOLETIM_OCORRENCIA
        consulta.valor = '{}' if FAKE else google_vision.Service().detect_text(url)
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
    consultar_numero_chassi2(validacao)
    consultar_caracteristicas_chassi(validacao)
    consultar_presenca_proprietario(validacao)
    consultar_cor_veiculo(validacao)
    consultar_procuracao(validacao)
    consultar_boletim_ocorrencia(validacao)