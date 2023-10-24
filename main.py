"""
Ponto de entrada da aplicação.
"""
import pandas as pd
import msc_tester.app, msc_tester.reporter
from msc_tester.test import test1, test2, test3, test4, test5, test6, test7, test8, test9, test11
import logging as logger
import os

ano = input('Digite o ANO desejado [AAAA]: ')
mes = input('Digite o MÊS desejado [MM]: ').zfill(2)

if mes == '01':
    ano_anterior = str(int(ano) - 1)
else:
    ano_anterior = ano

mes_anterior = str(int(mes) - 1).zfill(2)
if mes_anterior == '00':
    mes_anterior_msc = '13'
    mes_anterior_pad = '12'
else:
    mes_anterior_msc = mes_anterior
    mes_anterior_pad = mes_anterior

logger.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=logger.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
file_report = r'report.xlsx'
file_mapeamento_cc = r'mapeamento_cc.xlsx'
file_msc_atual = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\MSC\parquet', f'{ano}-{mes}.parquet')
file_msc_anterior = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\MSC\parquet', f'{ano_anterior}-{mes_anterior_msc}.parquet')
file_balver_atual = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\PAD', f'{ano}-{mes}', r'parquet\BAL_VER.parquet')
if mes_anterior_msc == '13':
    file_balver_anterior = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\PAD', f'{ano_anterior}-{mes_anterior_pad}', r'parquet\BVER_ENC.parquet')
else:
    file_balver_anterior = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\PAD', f'{ano_anterior}-{mes_anterior_pad}', r'parquet\BAL_VER.parquet')
file_balrec = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\PAD', f'{ano}-{mes}', r'parquet\BAL_REC.parquet')
file_baldesp = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\PAD', f'{ano}-{mes}', r'parquet\BAL_DESP.parquet')
file_decreto = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\PAD', f'{ano}-{mes}', r'parquet\DECRETO.parquet')
file_restos_pagar = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\PAD', f'{ano}-{mes}', r'parquet\RESTOS_PAGAR.parquet')

logger.debug(f'Arquivo de resultados: {file_report}')
logger.debug(f'Arquivo de mapeamento de conta contábil: {file_mapeamento_cc}')
logger.debug(f'Arquivo da MSC atual: {file_msc_atual}')
logger.debug(f'Arquivo da MSC anterior: {file_msc_anterior}')
logger.debug(f'Arquivo do BAL_VER atual: {file_balver_atual}')
logger.debug(f'Arquivo do BAL_VER anterior: {file_balver_anterior}')
logger.debug(f'Arquivo do BAL_REC: {file_balrec}')
logger.debug(f'Arquivo do BAL_DESP: {file_baldesp}')
logger.debug(f'Arquivo do DECRETO: {file_decreto}')
logger.debug(f'Arquivo do RESTOS_PAGAR: {file_restos_pagar}')

reporter = msc_tester.reporter.ExcelReporter(file_report)
mapeamento_cc = pd.read_excel(file_mapeamento_cc, sheet_name='mapCC', dtype={'cc_pad': str, 'cc_msc': str})
msc_atual = pd.read_parquet(file_msc_atual)
msc_anterior = pd.read_parquet(file_msc_anterior)
balver_atual = pd.read_parquet(file_balver_atual)
balver_anterior = pd.read_parquet(file_balver_anterior)
balrec = pd.read_parquet(file_balrec)
baldesp = pd.read_parquet(file_baldesp)
decreto = pd.read_parquet(file_decreto)
restos_pagar = pd.read_parquet(file_restos_pagar)

testes = [
    test1,
    test2,
    test3,
    test4,
    test5,
    test6,
    test7,
    test8,
    test9,
    test11
]

app = msc_tester.app.App(logger, reporter, mapeamento_cc, msc_atual, msc_anterior, balver_atual, balver_anterior, balrec, baldesp, decreto, restos_pagar, testes, mes)
app.run()
