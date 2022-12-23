"""
Controlador geral da aplicação.
"""
import sqlite3


class App:
    def __init__(self, logger, reporter, mapeamento, msc_atual, msc_anterior, testes):
        self.logger = logger
        self.reporter = reporter
        self.mapeamento = mapeamento
        self.msc_anterior = msc_anterior
        self.msc_atual = msc_atual
        self.testes = testes


    def run(self):
        self.logger.info('Execução dos testes iniciada...')

        for t in self.testes:
            test = t.Test(app=self)
            self.logger.info(f'Executando teste {test.name}...')
            result = test.run()
            self.reporter.write(result, test.name)
        self.reporter.save()