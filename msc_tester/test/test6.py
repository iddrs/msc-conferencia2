"""
Testa se os saldos relativos à receita orçamentária estão corretos.

Considera apenas os valores totais.

"""
import pandas as pd
from tqdm import tqdm


class Test:
    def __init__(self, app):
        self.name = 'receita_orcamentaria'
        self.app = app

    def run(self):
        self.app.logger.debug('Preparando o BAL_REC...')
        balrec = self.prepare_balrec(self.app.balrec)
        self.app.logger.debug('Realizando o teste...')

        result = self.run_test(self.app.msc_atual, balrec)
        self.app.logger.debug('Devolvendo o resultado...')
        return result

    def prepare_balrec(self, balrec):
        balrec['receita_orcada'] = balrec['receita_orcada'].fillna(0.0)
        balrec['receita_realizada'] = balrec['receita_realizada'].fillna(0.0)
        balrec['previsao_atualizada'] = balrec['previsao_atualizada'].fillna(0.0)
        balrec['receita_a_arrecadar'] = balrec['receita_a_arrecadar'].fillna(0.0)
        balrec['valor_atualizacao'] = balrec['valor_atualizacao'].fillna(0.0)
        return balrec


    def run_test(self, msc, balrec):
        result = []
        total = 13
        with tqdm(total=total) as progressbar:
            # PREVISAO INICIAL DA RECEITA BRUTA
            result.append(self.teste1(msc, balrec))
            progressbar.update(1)

            # PREVISÃO DE DEDUÇÕES DA RECEITA: FUNDEB
            result.append(self.teste2(msc, balrec))
            progressbar.update(1)

            # PREVISÃO DE DEDUÇÕES DA RECEITA: RENÚNCIA
            result.append(self.teste3(msc, balrec))
            progressbar.update(1)

            # PREVISÃO DE DEDUÇÕES DA RECEITA: OUTRAS
            result.append(self.teste4(msc, balrec))
            progressbar.update(1)

            # PREVISÃO ADICIONAL DA RECEITA: REESTIMATIVA
            result.append(self.teste5(msc, balrec))
            progressbar.update(1)

            # PREVISÃO DE DEDUÇÕES DA RECEITA POR TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS: FUNDEB
            result.append(self.teste6(msc, balrec))
            progressbar.update(1)

            # PREVISÃO DE DEDUÇÕES DA RECEITA: RENÚNCIA
            result.append(self.teste7(msc, balrec))
            progressbar.update(1)

            # PREVISÃO DE DEDUÇÕES DA RECEITA: OUTRAS
            result.append(self.teste8(msc, balrec))
            progressbar.update(1)

            # RECEITA A REALIZAR
            result.append(self.teste9(msc, balrec))
            progressbar.update(1)

            # RECEITA REALIZADA BRUTA
            result.append(self.teste10(msc, balrec))
            progressbar.update(1)

            # DEDUÇÕES DA RECEITA ORÇAMENTÁRIA: FUNDEB
            result.append(self.teste11(msc, balrec))
            progressbar.update(1)

            # DEDUÇÕES DA RECEITA ORÇAMENTÁRIA: RENÚNCIA
            result.append(self.teste12(msc, balrec))
            progressbar.update(1)

            # DEDUÇÕES DA RECEITA ORÇAMENTÁRIA: OUTRAS
            result.append(self.teste13(msc, balrec))
            progressbar.update(1)

        df = pd.DataFrame(result)
        return df

    def teste1(self, msc, balrec):
        # self.app.logger.debug('Testando a PREVISAO INICIAL DA RECEITA BRUTA...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '521110000')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '521110000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_balrec = round(sum(balrec[
                                     (balrec['tipo_nivel_receita'] == 'A')
                                     & (balrec['caracteristica_peculiar_receita'] == 0)
                                 ]['receita_orcada']), 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'PREVISAO INICIAL DA RECEITA BRUTA',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }


    def teste2(self, msc, balrec):
        # self.app.logger.debug('Testando a PREVISÃO DE DEDUÇÕES DA RECEITA: FUNDEB...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '521120101')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '521120101')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_balrec = round(sum(balrec[
                                     (balrec['recurso_vinculado'] == 31)
                                     & (balrec['caracteristica_peculiar_receita'] > 0)
                                 ]['receita_orcada'])*-1, 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'PREVISÃO DE DEDUÇÕES DA RECEITA: FUNDEB',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }

    def teste3(self, msc, balrec):
        # self.app.logger.debug('Testando a PREVISÃO DE DEDUÇÕES DA RECEITA: RENÚNCIA...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '521120200')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '521120200')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_balrec = round(sum(balrec[
                                     (balrec['recurso_vinculado'] > 0)
                                     & (balrec['caracteristica_peculiar_receita'] > 0)
                                     & (
                                             (balrec['caracteristica_peculiar_receita'] == 101)
                                             | (balrec['caracteristica_peculiar_receita'] == 103)
                                     )
                                 ]['receita_orcada'])*-1, 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'PREVISÃO DE DEDUÇÕES DA RECEITA: RENÚNCIA',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }

    def teste4(self, msc, balrec):
        # self.app.logger.debug('Testando a PREVISÃO DE DEDUÇÕES DA RECEITA: OUTRAS...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '521129900')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '521129900')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_balrec = round(sum(balrec[
                                     (balrec['recurso_vinculado'] > 0)
                                     & (balrec['caracteristica_peculiar_receita'] > 0)
                                     & (
                                         (balrec['caracteristica_peculiar_receita'] != 101)
                                         & (balrec['caracteristica_peculiar_receita'] != 103)
                                         & (balrec['caracteristica_peculiar_receita'] != 105)
                                     )
                                 ]['receita_orcada'])*-1, 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'PREVISÃO DE DEDUÇÕES DA RECEITA: OUTRAS',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }

    def teste5(self, msc, balrec):
        # self.app.logger.debug('Testando a PREVISÃO ADICIONAL DA RECEITA: REESTIMATIVA...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '521210100')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '521210100')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_balrec = round(sum(balrec[
                                     (balrec['tipo_nivel_receita'] == 'A')
                                     # & (balrec['caracteristica_peculiar_receita'] == 0)
                                 ]['valor_atualizacao']), 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'PREVISÃO ADICIONAL DA RECEITA: REESTIMATIVA',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }

    def teste6(self, msc, balrec):
        # self.app.logger.debug('Testando a PREVISÃO DE DEDUÇÕES DA RECEITA POR TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS: FUNDEB...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '521210301')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '521210301')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_balrec = round(sum(balrec[
                                     (balrec['recurso_vinculado'] ==31)
                                     & (balrec['caracteristica_peculiar_receita'] == 105)
                                 ]['valor_atualizacao'])*-1, 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'PREVISÃO DE DEDUÇÕES DA RECEITA POR TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS: FUNDEB',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }

    def teste7(self, msc, balrec):
        # self.app.logger.debug('Testando a PREVISÃO DE DEDUÇÕES DA RECEITA: RENÚNCIA...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '521210400')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '521210400')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_balrec = round(sum(balrec[
                                     (balrec['recurso_vinculado'] > 0)
                                     & (
                                         (balrec['caracteristica_peculiar_receita'] == 101)
                                         | (balrec['caracteristica_peculiar_receita'] == 103)
                                     )

                                 ]['valor_atualizacao'])*-1, 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'PREVISÃO DE DEDUÇÕES DA RECEITA: RENÚNCIA',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }

    def teste8(self, msc, balrec):
        # self.app.logger.debug('Testando a PREVISÃO DE DEDUÇÕES DA RECEITA: OUTRAS...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '521219900')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '521219900')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_balrec = round(sum(balrec[
                                     (balrec['recurso_vinculado'] > 0)
                                     & (
                                         (balrec['caracteristica_peculiar_receita'] != 101)
                                         & (balrec['caracteristica_peculiar_receita'] == 103)
                                         & (balrec['caracteristica_peculiar_receita'] == 105)
                                     )

                                 ]['valor_atualizacao'])*-1, 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'PREVISÃO DE DEDUÇÕES DA RECEITA: OUTRAS',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }

    def teste9(self, msc, balrec):
        # self.app.logger.debug('Testando a RECEITA A REALIZAR...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '621100000')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '621100000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_balrec = round(sum(balrec[
                                     (balrec['tipo_nivel_receita'] == 'A')
                                 ]['receita_a_arrecadar']), 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'RECEITA A REALIZAR',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }

    def teste10(self, msc, balrec):
        # self.app.logger.debug('Testando a RECEITA REALIZADA BRUTA...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '621200000')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '621200000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_balrec = round(sum(balrec[
                                     (balrec['tipo_nivel_receita'] == 'A')
                                     & (balrec['caracteristica_peculiar_receita'] == 0)
                                 ]['receita_realizada']), 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'RECEITA REALIZADA BRUTA',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }

    def teste11(self, msc, balrec):
        # self.app.logger.debug('Testando a DEDUÇÕES DA RECEITA ORÇAMENTÁRIA: FUNDEB...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '621310100')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '621310100')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_balrec = round(sum(balrec[
                                     (balrec['caracteristica_peculiar_receita'] > 0)
                                     & (balrec['caracteristica_peculiar_receita'] == 105)
                                 ]['receita_realizada'])*-1, 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'DEDUÇÕES DA RECEITA ORÇAMENTÁRIA: FUNDEB',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }

    def teste12(self, msc, balrec):
        # self.app.logger.debug('Testando a DEDUÇÕES DA RECEITA ORÇAMENTÁRIA: RENÚNCIA...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '621320000')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '621320000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_balrec = round(sum(balrec[
                                     (balrec['caracteristica_peculiar_receita'] > 0)
                                     & (
                                         (balrec['caracteristica_peculiar_receita'] == 101)
                                         | (balrec['caracteristica_peculiar_receita'] == 103)
                                     )
                                 ]['receita_realizada'])*-1, 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'DEDUÇÕES DA RECEITA ORÇAMENTÁRIA: RENÚNCIA',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }

    def teste13(self, msc, balrec):
        # self.app.logger.debug('Testando a DEDUÇÕES DA RECEITA ORÇAMENTÁRIA: OUTRAS...')

        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '621390000')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['NR'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '621390000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['NR'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_balrec = round(sum(balrec[
                                     (balrec['caracteristica_peculiar_receita'] > 0)
                                     & (
                                         (balrec['caracteristica_peculiar_receita'] != 101)
                                         & (balrec['caracteristica_peculiar_receita'] != 103)
                                         & (balrec['caracteristica_peculiar_receita'] != 105)
                                         & (balrec['caracteristica_peculiar_receita'] != 0)
                                     )
                                 ]['receita_realizada'])*-1, 2)
        diff = round(saldo_msc - saldo_balrec, 2)
        # print(saldo_msc, saldo_balrec)
        return {
            'teste': 'DEDUÇÕES DA RECEITA ORÇAMENTÁRIA: OUTRAS',
            'valor_msc': saldo_msc,
            'valor_balrec': saldo_balrec,
            'diff': diff
        }