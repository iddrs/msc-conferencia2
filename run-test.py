"""
Ponto de entrada da aplicação.
"""
import pandas as pd
import msc_tester.app, msc_tester.reporter
from msc_tester.test import test1
import logging as logger

logger.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=logger.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

reporter = msc_tester.reporter.ExcelReporter(r'report.xlsx')

mapeamento = pd.read_csv(r'mapeamento.csv', sep=';', dtype={'pad': str, 'msc': str})

msc_atual = pd.read_pickle(r'C:\Users\Everton\Desktop\Prefeitura\MSC\v2\pickle\2022-11.pickle')

msc_anterior = pd.read_pickle(r'C:\Users\Everton\Desktop\Prefeitura\MSC\v2\pickle\2022-10.pickle')

testes = [
    test1,
]

app = msc_tester.app.App(logger, reporter, mapeamento, msc_atual, msc_anterior, testes)
app.run()
