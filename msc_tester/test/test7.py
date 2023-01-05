"""
Testa se os saldos relativos à despesa orçamentária estão corretos.

Considera apenas os valores totais.

"""
import pandas as pd
from tqdm import tqdm


class Test:
    def __init__(self, app):
        self.name = 'despesa_orcamentaria'
        self.app = app

    def run(self):
        self.app.logger.debug('Preparando o BAL_DESP...')
        baldesp = self.prepare_baldesp(self.app.baldesp)
        self.app.logger.debug('Realizando o teste...')

        result = self.run_test(self.app.msc_atual, baldesp)
        self.app.logger.debug('Devolvendo o resultado...')
        return result

    def prepare_baldesp(self, baldesp):
        # balrec['receita_orcada'] = balrec['receita_orcada'].fillna(0.0)
        # balrec['receita_realizada'] = balrec['receita_realizada'].fillna(0.0)
        # balrec['previsao_atualizada'] = balrec['previsao_atualizada'].fillna(0.0)
        # balrec['receita_a_arrecadar'] = balrec['receita_a_arrecadar'].fillna(0.0)
        # balrec['valor_atualizacao'] = balrec['valor_atualizacao'].fillna(0.0)
        return baldesp


    def run_test(self, msc, baldesp):
        result = []
        total = 9
        with tqdm(total=total) as progressbar:
            # CREDITO INICIAL
            result.append(self.teste1(msc, baldesp))
            progressbar.update(1)

            # EMPENHOS POR EMISSÃO
            result.append(self.teste2(msc, baldesp))
            progressbar.update(1)

            # CREDITO DISPONÍVEL
            result.append(self.teste3(msc, baldesp))
            progressbar.update(1)

            # CREDITO EMPENHADO A LIQUIDAR
            result.append(self.teste4(msc, baldesp))
            progressbar.update(1)

            # CREDITO EMPENHADO LIQUIDADO A PAGAR
            result.append(self.teste5(msc, baldesp))
            progressbar.update(1)

            # CREDITO EMPENHADO LIQUIDADO PAGO
            result.append(self.teste6(msc, baldesp))
            progressbar.update(1)

            # EMPENHOS A LIQUIDAR
            result.append(self.teste7(msc, baldesp))
            progressbar.update(1)

            # EMPENHOS LIQUIDADOS A PAGAR
            result.append(self.teste8(msc, baldesp))
            progressbar.update(1)

            # EMPENHOS LIQUIDADOS PAGOS
            result.append(self.teste9(msc, baldesp))
            progressbar.update(1)

        df = pd.DataFrame(result)
        return df

    def teste1(self, msc, baldesp):
        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '522110100')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                                  & (msc['ND'].notnull())
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '522110100')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_baldesp = round(sum(baldesp['dotacao_inicial']), 2)
        diff = round(saldo_msc - saldo_baldesp, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_baldesp}', f'DIF: {diff}')
        return {
            'teste': 'CREDITO INICIAL',
            'valor_msc': saldo_msc,
            'valor_baldesp': saldo_baldesp,
            'diff': diff
        }


    def teste2(self, msc, baldesp):
        saldo_msc_d = round(sum(msc[
                                    (msc.ContaContabil.str.startswith('52292'))
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    # Necessário comentar porque nem todos os registros tem valor em ND
                                    # & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc.ContaContabil.str.startswith('52292'))
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    # Necessário comentar porque nem todos os registros tem valor em ND
                                    # & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_baldesp = round(sum(baldesp['valor_empenhado']), 2)
        diff = round(saldo_msc - saldo_baldesp, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_baldesp}', f'DIF: {diff}')
        return {
            'teste': 'EMPENHOS POR EMISSÃO',
            'valor_msc': saldo_msc,
            'valor_baldesp': saldo_baldesp,
            'diff': diff
        }

    def teste3(self, msc, baldesp):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '622110000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '622110000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_baldesp = round(sum(baldesp['dotacao_a_empenhar']), 2)
        diff = round(saldo_msc - saldo_baldesp, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_baldesp}', f'DIF: {diff}')
        return {
            'teste': 'CREDITO DISPONÍVEL',
            'valor_msc': saldo_msc,
            'valor_baldesp': saldo_baldesp,
            'diff': diff
        }

    def teste4(self, msc, baldesp):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '622130100')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '622130100')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_baldesp = round(sum(baldesp['empenhado_a_liquidar']), 2)
        diff = round(saldo_msc - saldo_baldesp, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_baldesp}', f'DIF: {diff}')
        return {
            'teste': 'CREDITO EMPENHADO A LIQUIDAR',
            'valor_msc': saldo_msc,
            'valor_baldesp': saldo_baldesp,
            'diff': diff
        }

    def teste5(self, msc, baldesp):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '622130300')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '622130300')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_baldesp = round(sum(baldesp['liquidado_a_pagar']), 2)
        diff = round(saldo_msc - saldo_baldesp, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_baldesp}', f'DIF: {diff}')
        return {
            'teste': 'CREDITO EMPENHADO LIQUIDADO A PAGAR',
            'valor_msc': saldo_msc,
            'valor_baldesp': saldo_baldesp,
            'diff': diff
        }

    def teste6(self, msc, baldesp):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '622130400')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '622130400')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_baldesp = round(sum(baldesp['valor_pago']), 2)
        diff = round(saldo_msc - saldo_baldesp, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_baldesp}', f'DIF: {diff}')
        return {
            'teste': 'CREDITO EMPENHADO LIQUIDADO PAGO',
            'valor_msc': saldo_msc,
            'valor_baldesp': saldo_baldesp,
            'diff': diff
        }

    def teste7(self, msc, baldesp):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '622920101')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    # Comentado porque nem todas as linhas tem ND
                                    # & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '622920101')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    # Comentado porque nem todas as linhas tem ND
                                    # & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_baldesp = round(sum(baldesp['empenhado_a_liquidar']), 2)
        diff = round(saldo_msc - saldo_baldesp, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_baldesp}', f'DIF: {diff}')
        return {
            'teste': 'EMPENHOS A LIQUIDAR',
            'valor_msc': saldo_msc,
            'valor_baldesp': saldo_baldesp,
            'diff': diff
        }

    def teste8(self, msc, baldesp):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '622920103')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    # Comentado porque nem todas as linhas tem ND
                                    # & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '622920103')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    # Comentado porque nem todas as linhas tem ND
                                    # & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_baldesp = round(sum(baldesp['liquidado_a_pagar']), 2)
        diff = round(saldo_msc - saldo_baldesp, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_baldesp}', f'DIF: {diff}')
        return {
            'teste': 'EMPENHOS LIQUIDADOS A PAGAR',
            'valor_msc': saldo_msc,
            'valor_baldesp': saldo_baldesp,
            'diff': diff
        }

    def teste9(self, msc, baldesp):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '622920104')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    # Comentado porque nem todas as linhas tem ND
                                    # & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '622920104')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    # Comentado porque nem todas as linhas tem ND
                                    # & (msc['ND'].notnull())
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_baldesp = round(sum(baldesp['valor_pago']), 2)
        diff = round(saldo_msc - saldo_baldesp, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_baldesp}', f'DIF: {diff}')
        return {
            'teste': 'EMPENHOS LIQUIDADOS PAGOS',
            'valor_msc': saldo_msc,
            'valor_baldesp': saldo_baldesp,
            'diff': diff
        }