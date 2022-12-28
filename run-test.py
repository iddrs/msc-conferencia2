"""
Ponto de entrada da aplicação.
"""
import pandas as pd
import msc_tester.app, msc_tester.reporter
from msc_tester.test import test1, test2, test3, test4, test5
import logging as logger

logger.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=logger.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

reporter = msc_tester.reporter.ExcelReporter(r'report.xlsx')

mapeamento_cc = pd.read_excel(r'mapeamento_cc.xlsx', sheet_name='mapCC', dtype={'cc_pad': str, 'cc_msc': str})

msc_atual = pd.read_pickle(r'C:\Users\Everton\Desktop\Prefeitura\MSC\v2\pickle\2022-11.pickle')

msc_anterior = pd.read_pickle(r'C:\Users\Everton\Desktop\Prefeitura\MSC\v2\pickle\2022-10.pickle')

balver_atual = pd.read_pickle(r'C:\Users\Everton\Desktop\Prefeitura\PAD\v2\2022-11\pickle\BAL_VER.pickle')

balver_anterior  = pd.read_pickle(r'C:\Users\Everton\Desktop\Prefeitura\PAD\v2\2022-10\pickle\BAL_VER.pickle')

testes = [
    test1,
    test2,
    test3,
    test4,
    test5,
]

app = msc_tester.app.App(logger, reporter, mapeamento_cc, msc_atual, msc_anterior, balver_atual, balver_anterior, testes)
app.run()
