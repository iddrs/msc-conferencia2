"""
Testa se os saldos relativos as alterações da dotação estão corretos.

Considera apenas os valores totais.

"""
import pandas as pd
from tqdm import tqdm


class Test:
    def __init__(self, app):
        self.name = 'dotacao'
        self.app = app

    def run(self):
        self.app.logger.debug('Preparando o DECRETO...')
        decreto = self.prepare_decreto(self.app.decreto)
        self.app.logger.debug('Realizando o teste...')

        result = self.run_test(self.app.msc_atual, decreto)
        self.app.logger.debug('Devolvendo o resultado...')
        return result

    def prepare_decreto(self, decreto):
        # balrec['receita_orcada'] = balrec['receita_orcada'].fillna(0.0)
        # balrec['receita_realizada'] = balrec['receita_realizada'].fillna(0.0)
        # balrec['previsao_atualizada'] = balrec['previsao_atualizada'].fillna(0.0)
        # balrec['receita_a_arrecadar'] = balrec['receita_a_arrecadar'].fillna(0.0)
        # balrec['valor_atualizacao'] = balrec['valor_atualizacao'].fillna(0.0)
        return decreto


    def run_test(self, msc, decreto):
        result = []
        total = 9
        with tqdm(total=total) as progressbar:
            # CREDITO INICIAL
            result.append(self.teste1(msc, decreto))
            progressbar.update(1)

            # EMPENHOS POR EMISSÃO
            result.append(self.teste2(msc, decreto))
            progressbar.update(1)

            # CREDITO DISPONÍVEL
            result.append(self.teste3(msc, decreto))
            progressbar.update(1)

            # CREDITO EMPENHADO A LIQUIDAR
            result.append(self.teste4(msc, decreto))
            progressbar.update(1)

            # CREDITO EMPENHADO LIQUIDADO A PAGAR
            result.append(self.teste5(msc, decreto))
            progressbar.update(1)

            # CREDITO EMPENHADO LIQUIDADO PAGO
            result.append(self.teste6(msc, decreto))
            progressbar.update(1)

            # EMPENHOS A LIQUIDAR
            result.append(self.teste7(msc, decreto))
            progressbar.update(1)

            # EMPENHOS LIQUIDADOS A PAGAR
            result.append(self.teste8(msc, decreto))
            progressbar.update(1)

            # EMPENHOS LIQUIDADOS PAGOS
            result.append(self.teste9(msc, decreto))
            progressbar.update(1)

        df = pd.DataFrame(result)
        return df

    def teste1(self, msc, decreto):
        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '522120100')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '522120100')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_decreto = round(sum(decreto[
                                      (decreto['tipo_credito_adicional'] == 1)
                                  ]['valor_credito_adicional']), 2)
        diff = round(saldo_msc - saldo_decreto, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_decreto}', f'DIF: {diff}')
        return {
            'teste': 'CREDITO ADICIONAL - SUPLEMENTAR',
            'valor_msc': saldo_msc,
            'valor_decreto': saldo_decreto,
            'diff': diff
        }


    def teste2(self, msc, decreto):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '522120201')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '522120201')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_decreto = round(sum(decreto[
                                      (decreto['tipo_credito_adicional'] == 2)
                                      & (decreto['data_reabertura'].isnull())
                                  ]['valor_credito_adicional']), 2)
        diff = round(saldo_msc - saldo_decreto, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_decreto}', f'DIF: {diff}')
        return {
            'teste': 'CRÉDITOS ESPECIAIS ABERTOS',
            'valor_msc': saldo_msc,
            'valor_decreto': saldo_decreto,
            'diff': diff
        }

    def teste3(self, msc, decreto):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '522120202')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '522120202')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_decreto = round(sum(decreto[
                                      (decreto['tipo_credito_adicional'] == 2)
                                      & (decreto['data_reabertura'].notnull())
                                      ]['valor_credito_adicional']), 2)
        diff = round(saldo_msc - saldo_decreto, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_decreto}', f'DIF: {diff}')
        return {
            'teste': 'CRÉDITOS ESPECIAIS REABERTOS',
            'valor_msc': saldo_msc,
            'valor_decreto': saldo_decreto,
            'diff': diff
        }

    def teste4(self, msc, decreto):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '522120301')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '522120301')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_decreto = round(sum(decreto[
                                      (decreto['tipo_credito_adicional'] == 3)
                                      ]['valor_credito_adicional']), 2)
        diff = round(saldo_msc - saldo_decreto, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_decreto}', f'DIF: {diff}')
        return {
            'teste': 'CRÉDITOS EXTRAORDINÁRIOS ABERTOS',
            'valor_msc': saldo_msc,
            'valor_decreto': saldo_decreto,
            'diff': diff
        }

    def teste5(self, msc, decreto):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '522130100')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '522130100')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_decreto = round(sum(decreto[
                                      (decreto['origem_recurso'] == 1)
                                  ]['valor_credito_adicional']), 2)
        diff = round(saldo_msc - saldo_decreto, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_decreto}', f'DIF: {diff}')
        return {
            'teste': 'SUPERAVIT FINANCEIRO DE EXERCÍCIO ANTERIOR',
            'valor_msc': saldo_msc,
            'valor_decreto': saldo_decreto,
            'diff': diff
        }

    def teste6(self, msc, decreto):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '522130200')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '522130200')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_decreto = round(sum(decreto[
                                      (decreto['origem_recurso'] == 2)
                                  ]['valor_credito_adicional']), 2)
        diff = round(saldo_msc - saldo_decreto, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_decreto}', f'DIF: {diff}')
        return {
            'teste': 'EXCESSO DE ARRECADAÇÃO',
            'valor_msc': saldo_msc,
            'valor_decreto': saldo_decreto,
            'diff': diff
        }

    def teste7(self, msc, decreto):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '522130300')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '522130300')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_decreto = round(sum(decreto[
                                      (
                                          (decreto['origem_recurso'] == 5)
                                          | (decreto['origem_recurso'] == 6)
                                      )
                                  ]['valor_credito_adicional']), 2)
        diff = round(saldo_msc - saldo_decreto, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_decreto}', f'DIF: {diff}')
        return {
            'teste': 'ANULAÇÃO DE DOTAÇÃO',
            'valor_msc': saldo_msc,
            'valor_decreto': saldo_decreto,
            'diff': diff
        }

    def teste8(self, msc, decreto):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '522130400')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '522130400')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_decreto = round(sum(decreto[
                                      (decreto['origem_recurso'] == 3)
                                  ]['valor_credito_adicional']), 2)
        diff = round(saldo_msc - saldo_decreto, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_decreto}', f'DIF: {diff}')
        return {
            'teste': 'OPERAÇÕES DE CRÉDITO',
            'valor_msc': saldo_msc,
            'valor_decreto': saldo_decreto,
            'diff': diff
        }

    def teste9(self, msc, decreto):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '522130600')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '522130600')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_decreto = round(sum(decreto[
                                      (decreto['tipo_credito_adicional'] == 2)
                                      & (decreto['data_reabertura'].notnull())
                                      ]['valor_credito_adicional']), 2)
        diff = round(saldo_msc - saldo_decreto, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_decreto}', f'DIF: {diff}')
        return {
            'teste': 'DOTAÇÃO TRANSFERIDA',
            'valor_msc': saldo_msc,
            'valor_decreto': saldo_decreto,
            'diff': diff
        }