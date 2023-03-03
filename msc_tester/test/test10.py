"""
Testa se os saldos dos grupos 5 e 6 que precisa estar zerados estão zerados.

Considera apenas os valores totais.

"""
import pandas as pd
from tqdm import tqdm


class Test:
    def __init__(self, app):
        self.name = 'orcamentario_saldo_zero'
        self.app = app

    def run(self):
        self.app.logger.debug('Realizando o teste...')

        result = self.run_test(self.app.msc_atual)
        self.app.logger.debug('Devolvendo o resultado...')
        return result

    def run_test(self, msc):
        result = []
        total = 4
        with tqdm(total=total) as progressbar:
            # Grupo 5.1
            result.append(self.teste1(msc))
            progressbar.update(1)

            # Grupo 5.2
            result.append(self.teste2(msc))
            progressbar.update(1)

            # Grupo 6.1
            result.append(self.teste3(msc))
            progressbar.update(1)

            # Grupo 6.2
            result.append(self.teste4(msc))
            progressbar.update(1)


        df = pd.DataFrame(result)
        return df

    def retorna_saldo(self, msc, cc):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'].str.startswith(cc))
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'].str.startswith(cc))
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c
        return saldo_msc

    def teste1(self, msc):
        saldo_msc = self.retorna_saldo(msc, '51')

        diff = round(saldo_msc - 0.0, 2)
        return {
            'teste': 'Grupo 5.1.* zerado',
            'valor_msc': saldo_msc,
            'valor_esperado': 0.0,
            'diff': diff
        }

    def teste2(self, msc):
        saldo_msc = self.retorna_saldo(msc, '52')

        diff = round(saldo_msc - 0.0, 2)
        return {
            'teste': 'Grupo 5.2.* zerado',
            'valor_msc': saldo_msc,
            'valor_esperado': 0.0,
            'diff': diff
        }

    def teste3(self, msc):
        saldo_msc = self.retorna_saldo(msc, '61')

        diff = round(saldo_msc - 0.0, 2)
        return {
            'teste': 'Grupo 6.1.* zerado',
            'valor_msc': saldo_msc,
            'valor_esperado': 0.0,
            'diff': diff
        }

    def teste4(self, msc):
        saldo_msc = self.retorna_saldo(msc, '62')

        diff = round(saldo_msc - 0.0, 2)
        return {
            'teste': 'Grupo 6.2.* zerado',
            'valor_msc': saldo_msc,
            'valor_esperado': 0.0,
            'diff': diff
        }