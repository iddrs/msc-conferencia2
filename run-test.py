"""
Ponto de entrada da aplicação.
"""
import pandas as pd
import msc_tester.app, msc_tester.reporter
from msc_tester.test import test1, test2, test3, test4, test5, test6
import logging as logger
import os

mes = input('Digite o MÊS desejado [MM]: ').zfill(2)
ano = input('Digite o ANO desejado [AAAA]: ')

if mes == '01':
    ano_anterior = str(int(ano) - 1)
else:
    ano_anterior = ano

mes_anterior = str(int(mes) - 1).zfill(2)
if mes_anterior == '00':
    mes_anterior = '12'

logger.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=logger.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
file_report = r'report.xlsx'
file_mapeamento_cc = r'mapeamento_cc.xlsx'
file_msc_atual = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\MSC\v2\pickle', f'{ano}-{mes}.pickle')
file_msc_anterior = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\MSC\v2\pickle', f'{ano_anterior}-{mes_anterior}.pickle')
file_balver_atual = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\PAD\v2', f'{ano}-{mes}', r'pickle\BAL_VER.pickle')
file_balver_anterior = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\PAD\v2', f'{ano_anterior}-{mes_anterior}', r'pickle\BAL_VER.pickle')
file_balrec = os.path.join(r'C:\Users\Everton\Desktop\Prefeitura\PAD\v2', f'{ano}-{mes}', r'pickle\BAL_REC.pickle')

logger.debug(f'Arquivo de resultados: {file_report}')
logger.debug(f'Arquivo de mapeamento de conta contábil: {file_mapeamento_cc}')
logger.debug(f'Arquivo da MSC atual: {file_msc_atual}')
logger.debug(f'Arquivo da MSC anterior: {file_msc_anterior}')
logger.debug(f'Arquivo do BAL_VER atual: {file_balver_atual}')
logger.debug(f'Arquivo do BAL_VER anterior: {file_balver_anterior}')
logger.debug(f'Arquivo do BAL_REC: {file_balrec}')

reporter = msc_tester.reporter.ExcelReporter(file_report)
mapeamento_cc = pd.read_excel(file_mapeamento_cc, sheet_name='mapCC', dtype={'cc_pad': str, 'cc_msc': str})
msc_atual = pd.read_pickle(file_msc_atual)
msc_anterior = pd.read_pickle(file_msc_anterior)
balver_atual = pd.read_pickle(file_balver_atual)
balver_anterior = pd.read_pickle(file_balver_anterior)
balrec = pd.read_pickle(file_balrec)

testes = [
    test1,
    test2,
    test3,
    test4,
    test5,
    test6,
]

app = msc_tester.app.App(logger, reporter, mapeamento_cc, msc_atual, msc_anterior, balver_atual, balver_anterior, balrec, testes)
app.run()
