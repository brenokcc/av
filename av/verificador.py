import json
from .models import Verificacao, Consulta, Cor, CodigoCor
import unicodedata

MAX_DISTANCE = 100
COLORS = {'WHITE': 'BRANCA', 'BLACK': 'PRETA', 'SILVER': 'PRATA', 'RED': 'VERMELHA', 'GRAY': 'CINZA', 'GREY': 'CINZA', 'YELLOW': 'AMARELA', 'BLUE': 'AZUL', 'GREEN': 'VERDE', 'BROWN': 'MARROM', 'ORANGE': 'LARANJA', 'BEIGE': 'BEGE', 'GOLDEN': 'DOURADA', 'FANTASY': 'FANTASIA', 'PURPLE': 'ROXA', 'PINK': 'ROSA'}
VALID_CHASSI_LABELS = ['METAL', 'MOTOR VEHICLE']
INVALID_CHASSI_LABELS = ['RECTANGLE', 'PATTERN', 'PAPER PRODUCT', 'EYEWEAR', 'PAPER', 'MONOCHROME PHOTOGRAPHY', 'LOGO', 'EVENT', 'BRAND', 'ROOM', 'CEILING', 'WINDOW', 'GLASS', 'WINDSHIELD', 'REFLECTION', 'TRANSPARENT MATERIAL', 'AUTOMOTIVE MIRROR', 'WINDSCREEN WIPER', 'ROAD', 'STREET']

def verificar_palavras(verificacao, consulta, texto):
   ausentes = []
   if consulta:
      texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode()
      valor = unicodedata.normalize('NFKD', consulta.valor).encode('ASCII', 'ignore').decode()
      for palavra in texto.split() if texto else []:
         if palavra not in valor:
            ausentes.append(palavra)
      if ausentes:
         verificacao.satisfeita = False
         verificacao.observacao = 'Não possui {}'.format(ausentes)
      else:
         verificacao.satisfeita = True
         verificacao.observacao = None
      verificacao.save()
   return ausentes

def verificar_compatibilidade(verificacao, consulta):
      verificacao.satisfeita = consulta.valor == 'MATCH' if consulta else False
      if verificacao.satisfeita:
         verificacao.observacao = None
      else:
         verificacao.observacao = 'Não confere'
      verificacao.save()

def verificar_rotulos_chassi(verificacao, consulta):
   if consulta:
      labels = json.loads(consulta.valor)
      for label in labels:
         if label.upper() in INVALID_CHASSI_LABELS:
            verificacao.satisfeita = False
            verificacao.observacao = 'Não deveria possuir rótulo "{}"'.format(label.upper())
            verificacao.save()
            return
      has_valid = False
      for label in VALID_CHASSI_LABELS:
         if label.upper() in labels:
            has_valid = True
            break
      if has_valid:
         verificacao.satisfeita = True
         verificacao.observacao = None
         verificacao.save()
      else:
         verificacao.satisfeita = False
         verificacao.observacao = 'Deveria possuir um dos rótulos {}'.format(VALID_CHASSI_LABELS)
         verificacao.save()

def verificar_geolocalizacao(verificacao):
   if verificacao.validacao.estampador and verificacao.validacao.latitude and verificacao.validacao.longitude:
      satisfeita = False
      observacao = []
      for local_instalacao in verificacao.validacao.estampador.localinstalacao_set.all():
         distancia = local_instalacao.calcular_distancia(verificacao.validacao.latitude, verificacao.validacao.longitude)
         if distancia < MAX_DISTANCE:
            satisfeita = True
            break
         else:
            observacao.append('{} ({} metros)'.format(local_instalacao, distancia))
      if satisfeita:
         verificacao.satisfeita = True
         verificacao.observacao = None
      else:
         verificacao.satisfeita = False
         verificacao.observacao = ' | '.join(observacao)
      verificacao.save()


def verificar_reconhecimento_operador(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.FOTO_OPERADOR).first()
   verificar_compatibilidade(verificacao, consulta)

def verificar_presenca_operador(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.PRESENCA_OPERADOR).first()
   verificar_compatibilidade(verificacao, consulta)

def verificar_nome_proprietario(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.DOCUMENTO_PROPRIETARIO).first()
   verificar_palavras(verificacao, consulta, verificacao.validacao.nome_proprietario.upper())

def verificar_cpf_proprietario(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.DOCUMENTO_PROPRIETARIO).first()
   verificar_palavras(verificacao, consulta, verificacao.validacao.nome_proprietario.upper())

def verificar_reconhecimento_proprietario(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.FOTO_PROPRIETARIO).first()
   verificar_compatibilidade(verificacao, consulta)

def verificar_presenca_proprietario(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.PRESENCA_PROPRIETARIO).first()
   verificar_compatibilidade(verificacao, consulta)

def verificar_nome_representante(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.DOCUMENTO_REPRESENTANTE).first()
   verificar_palavras(verificacao, consulta, verificacao.validacao.nome_representante.upper())


def verificar_cpf_representante(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.DOCUMENTO_REPRESENTANTE).first()
   verificar_palavras(verificacao, consulta, verificacao.validacao.cpf_representante.upper())

def verificar_reconhecimento_representante(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.FOTO_REPRESENTANTE).first()
   verificar_compatibilidade(verificacao, consulta)

def verificar_presenca_representante(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.PRESENCA_REPRESENTANTE).first()
   verificar_compatibilidade(verificacao, consulta)

def verificar_titulo_procuracao(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.PROCURACAO).first()
   verificar_palavras(verificacao, consulta, 'PROCURAÇÃO')

def verificar_dados_proprietario_procuracao(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.PROCURACAO).first()
   verificar_palavras(verificacao, consulta, '{} {}'.format(verificacao.validacao.nome_proprietario, verificacao.validacao.cpf_proprietario).upper())

def verificar_dados_representante_procuracao(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.PROCURACAO).first()
   verificar_palavras(verificacao, consulta,'{} {}'.format(verificacao.validacao.nome_representante, verificacao.validacao.cpf_representante).upper())

def verificar_placa_procuracao(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.PROCURACAO).first()
   verificar_palavras(verificacao, consulta, verificacao.validacao.placa.upper())

def verificar_assinatura_procuracao(verificacao):
   pass

def verificar_numero_chassi(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.NUMERO_CHASSI).first()
   verificar_palavras(verificacao, consulta, verificacao.validacao.chassi)
   if not verificacao.satisfeita:
      consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.NUMERO_CHASSI_2).first()
      verificar_palavras(verificacao, consulta, verificacao.validacao.chassi)


def verificar_caracteristica_chassi(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.CARACTERISTICAS_CHASSI).first()
   verificar_rotulos_chassi(verificacao, consulta)

def verificar_marca_veiculo(verificacao):
   marca = '{} {}'.format(verificacao.validacao.marca.nome, verificacao.validacao.marca.fabricante.nome)
   consulta1 = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.MARCA_FOTO_DIANTEIRA).first()
   consulta2 = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.MARCA_FOTO_TRASEIRA).first()
   verificar_palavras(verificacao, consulta1, marca)
   if not verificacao.satisfeita:
       verificar_palavras(verificacao, consulta2, marca)

def verificar_cor_veiculo(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.COR_VEICULO).first()
   if consulta:
      if CodigoCor.objects.filter(nome=consulta.valor, cores=verificacao.validacao.cor).exists():
          verificacao.satisfeita = True
          verificacao.observacao = None
      else:
         verificacao.satisfeita = False
         verificacao.observacao = 'Cor incopatível "{}"'.format(consulta.valor)
      verificacao.save()


def calcular_distancia(latitude, longitude):
   coords_1 = (self.latitude, self.longitude)
   coords_2 = (latitude, longitude)
   distancia = geopy.distance.geodesic(coords_1, coords_2)
   return distancia.m


def verificar_numero_placa_dianteira(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.FOTO_PLACA_DIANTEIRA).first()
   verificar_palavras(verificacao, consulta, '{} {}'.format(verificacao.validacao.placa.split('-')))

def verificar_itens_seguranca_placa_dianteira(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.OCR_PLACA_DIANTEIRA).first()
   verificar_palavras(verificacao, consulta, 'BR BRASIL')

def verificar_qrcode_placa_dianteira(verificacao):
   pass

def verificar_numero_placa_traseira(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.FOTO_PLACA_TRASEIRA).first()
   verificar_palavras(verificacao, consulta, '{} {}'.format(verificacao.validacao.placa.split('-')))

def verificar_itens_seguranca_placa_traseira(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.OCR_PLACA_TRASEIRA).first()
   verificar_palavras(verificacao, consulta, 'BR BRASIL')

def verificar_qrcode_placa_traseira(verificacao):
   pass

def verificar_numero_segunda_placa_traseira(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.FOTO_SEGUNDA_PLACA_TRASEIRA).first()
   verificar_palavras(verificacao, consulta, '{} {}'.format(verificacao.validacao.placa.split('-')))

def verificar_itens_segunda_seguranca_placa_traseira(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.OCR_SEGUNDA_PLACA_TRASEIRA).first()
   verificar_palavras(verificacao, consulta, 'BR BRASIL')

def verificar_qrcode_segunda_placa_traseira(verificacao):
   pass

def verificar_titulo_boletim_ocorrencia(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.BOLETIM_OCORRENCIA).first()
   verificar_palavras(verificacao, consulta, 'BOLETIM DE OCORRÊNCIA')

def verificar_dados_proprietario_boletim_ocorrencia(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.BOLETIM_OCORRENCIA).first()
   verificar_palavras(verificacao, consulta, '{} {}'.format(verificacao.validacao.nome_proprietario, verificacao.validacao.cpf_proprietario).upper())

def verificar_placa_boletim_ocorrencia(verificacao):
   consulta = verificacao.validacao.consulta_set.filter(valida=True, tipo=Consulta.BOLETIM_OCORRENCIA).first()
   verificar_palavras(verificacao, consulta, verificacao.validacao.placa.upper())

def verificar_descarte_placa_dianteira(verificacao):
   pass

def verificar_descarte_placa_traseira(verificacao):
   pass

def verificar_descarte_segunda_placa_traseira(verificacao):
   pass



def realizar_verificacoes(verificacao):
   if verificacao.descricao == Verificacao.GEOLOCALIZACAO and not verificacao.satisfeita:
      verificar_geolocalizacao(verificacao)
   if verificacao.descricao == Verificacao.RECONHECIMENTO_OPERADOR and not verificacao.satisfeita:
      verificar_reconhecimento_operador(verificacao)
   if verificacao.descricao == Verificacao.PRESENCA_OPERADOR and not verificacao.satisfeita:
      verificar_presenca_operador(verificacao)
   if verificacao.descricao == Verificacao.NOME_PROPRIETARIO and not verificacao.satisfeita:
      verificar_nome_proprietario(verificacao)
   if verificacao.descricao == Verificacao.CPF_PROPRIETARIO and not verificacao.satisfeita:
      verificar_cpf_proprietario(verificacao)
   if verificacao.descricao == Verificacao.RECONHECIMENTO_PROPRIETARIO and not verificacao.satisfeita:
      verificar_reconhecimento_proprietario(verificacao)
   if verificacao.descricao == Verificacao.PRESENCA_PROPRIETARIO and not verificacao.satisfeita:
      verificar_presenca_proprietario(verificacao)
   if verificacao.descricao == Verificacao.NOME_REPRESENTANTE and not verificacao.satisfeita:
      verificar_nome_representante(verificacao)
   if verificacao.descricao == Verificacao.CPF_REPRESENTANTE and not verificacao.satisfeita:
      verificar_cpf_representante(verificacao)
   if verificacao.descricao == Verificacao.RECONHECIMENTO_REPRESENTANTE and not verificacao.satisfeita:
      verificar_reconhecimento_representante(verificacao)
   if verificacao.descricao == Verificacao.PRESENCA_REPRESENTANTE and not verificacao.satisfeita:
      verificar_presenca_representante(verificacao)
   if verificacao.descricao == Verificacao.TITULO_PROCURACAO and not verificacao.satisfeita:
      verificar_titulo_procuracao(verificacao)
   if verificacao.descricao == Verificacao.DADOS_PROPRIETARIO_PROCURACAO and not verificacao.satisfeita:
      verificar_dados_proprietario_procuracao(verificacao)
   if verificacao.descricao == Verificacao.DADOS_REPRESENTANTE_PROCURACAO and not verificacao.satisfeita:
      verificar_dados_representante_procuracao(verificacao)
   if verificacao.descricao == Verificacao.PLACA_PROCURACAO and not verificacao.satisfeita:
      verificar_placa_procuracao(verificacao)
   if verificacao.descricao == Verificacao.ASSINATURA_PROCURACAO and not verificacao.satisfeita:
      verificar_assinatura_procuracao(verificacao)
   if verificacao.descricao == Verificacao.NUMERO_CHASSI and not verificacao.satisfeita:
      verificar_numero_chassi(verificacao)
   if verificacao.descricao == Verificacao.CARACTERISTICA_CHASSI and not verificacao.satisfeita:
      verificar_caracteristica_chassi(verificacao)
   if verificacao.descricao == Verificacao.MARCA_VEICULO and not verificacao.satisfeita:
      verificar_marca_veiculo(verificacao)
   if verificacao.descricao == Verificacao.COR_VEICULO and not verificacao.satisfeita:
      verificar_cor_veiculo(verificacao)
   if verificacao.descricao == Verificacao.NUMERO_PLACA_DIANTEIRA and not verificacao.satisfeita:
      verificar_numero_placa_dianteira(verificacao)
   if verificacao.descricao == Verificacao.ITENS_SEGURANCA_PLACA_DIANTEIRA and not verificacao.satisfeita:
      verificar_itens_seguranca_placa_dianteira(verificacao)
   if verificacao.descricao == Verificacao.QRCODE_PLACA_DIANTEIRA and not verificacao.satisfeita:
      verificar_qrcode_placa_dianteira(verificacao)
   if verificacao.descricao == Verificacao.NUMERO_PLACA_TRASEIRA and not verificacao.satisfeita:
      verificar_numero_placa_traseira(verificacao)
   if verificacao.descricao == Verificacao.ITENS_SEGURANCA_PLACA_TRASEIRA and not verificacao.satisfeita:
      verificar_itens_seguranca_placa_traseira(verificacao)
   if verificacao.descricao == Verificacao.QRCODE_PLACA_TRASEIRA and not verificacao.satisfeita:
      verificar_qrcode_placa_traseira(verificacao)
   if verificacao.descricao == Verificacao.NUMERO_SEGUNDA_PLACA_TRASEIRA and not verificacao.satisfeita:
      verificar_numero_segunda_placa_traseira(verificacao)
   if verificacao.descricao == Verificacao.ITENS_SEGUNDA_SEGURANCA_PLACA_TRASEIRA and not verificacao.satisfeita:
      verificar_itens_segunda_seguranca_placa_traseira(verificacao)
   if verificacao.descricao == Verificacao.QRCODE_SEGUNDA_PLACA_TRASEIRA and not verificacao.satisfeita:
      verificar_qrcode_segunda_placa_traseira(verificacao)
   if verificacao.descricao == Verificacao.TITULO_BOLETIM_OCORRENCIA and not verificacao.satisfeita:
      verificar_titulo_boletim_ocorrencia(verificacao)
   if verificacao.descricao == Verificacao.DADOS_PROPRIETARIO_BOLETIM_OCORRENCIA and not verificacao.satisfeita:
      verificar_dados_proprietario_boletim_ocorrencia(verificacao)
   if verificacao.descricao == Verificacao.PLACA_BOLETIM_OCORRENCIA and not verificacao.satisfeita:
      verificar_placa_boletim_ocorrencia(verificacao)
   if verificacao.descricao == Verificacao.DESCARTE_PLACA_DIANTEIRA and not verificacao.satisfeita:
      verificar_descarte_placa_dianteira(verificacao)
   if verificacao.descricao == Verificacao.DESCARTE_PLACA_TRASEIRA and not verificacao.satisfeita:
      verificar_descarte_placa_traseira(verificacao)
   if verificacao.descricao == Verificacao.DESCARTE_SEGUNDA_PLACA_TRASEIRA and not verificacao.satisfeita:
      verificar_descarte_segunda_placa_traseira(verificacao)
