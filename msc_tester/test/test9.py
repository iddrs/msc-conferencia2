"""
Testa se os saldos relativos aos restos a pagar estão corretos.

Considera apenas os valores totais.

"""
import pandas as pd
from tqdm import tqdm


class Test:
    def __init__(self, app):
        self.name = 'restos_pagar'
        self.app = app

    def run(self):
        self.app.logger.debug('Preparando o RESTOS_PAGAR...')
        restos_pagar = self.prepare_restos_pagar(self.app.restos_pagar)
        self.app.logger.debug('Realizando o teste...')

        result = self.run_test(self.app.msc_atual, restos_pagar)
        self.app.logger.debug('Devolvendo o resultado...')
        return result

    def prepare_restos_pagar(self, restos_pagar):
        # balrec['receita_orcada'] = balrec['receita_orcada'].fillna(0.0)
        # balrec['receita_realizada'] = balrec['receita_realizada'].fillna(0.0)
        # balrec['previsao_atualizada'] = balrec['previsao_atualizada'].fillna(0.0)
        # balrec['receita_a_arrecadar'] = balrec['receita_a_arrecadar'].fillna(0.0)
        # balrec['valor_atualizacao'] = balrec['valor_atualizacao'].fillna(0.0)
        return restos_pagar


    def run_test(self, msc, restos_pagar):
        result = []
        total = 15
        with tqdm(total=total) as progressbar:
            # CREDITO INICIAL
            result.append(self.teste1(msc, restos_pagar))
            progressbar.update(1)

            # EMPENHOS POR EMISSÃO
            result.append(self.teste2(msc, restos_pagar))
            progressbar.update(1)

            # CREDITO DISPONÍVEL
            result.append(self.teste3(msc, restos_pagar))
            progressbar.update(1)

            # CREDITO EMPENHADO A LIQUIDAR
            result.append(self.teste4(msc, restos_pagar))
            progressbar.update(1)

            # CREDITO EMPENHADO LIQUIDADO A PAGAR
            result.append(self.teste5(msc, restos_pagar))
            progressbar.update(1)

            # CREDITO EMPENHADO LIQUIDADO PAGO
            result.append(self.teste6(msc, restos_pagar))
            progressbar.update(1)

            # EMPENHOS A LIQUIDAR
            result.append(self.teste7(msc, restos_pagar))
            progressbar.update(1)

            # EMPENHOS LIQUIDADOS A PAGAR
            result.append(self.teste8(msc, restos_pagar))
            progressbar.update(1)

            # EMPENHOS LIQUIDADOS PAGOS
            result.append(self.teste9(msc, restos_pagar))
            progressbar.update(1)

            result.append(self.teste10(msc, restos_pagar))
            progressbar.update(1)

            result.append(self.teste11(msc, restos_pagar))
            progressbar.update(1)

            result.append(self.teste12(msc, restos_pagar))
            progressbar.update(1)

            result.append(self.teste13(msc, restos_pagar))
            progressbar.update(1)

            result.append(self.teste14(msc, restos_pagar))
            progressbar.update(1)

            result.append(self.teste15(msc, restos_pagar))
            progressbar.update(1)


        df = pd.DataFrame(result)
        return df

    def teste1(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                  (msc['ContaContabil'] == '531100000')
                                  & (msc['TipoValor'] == 'ending_balance')
                                  & (msc['NaturezaValor'] == 'D')
                              ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '531100000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_restos_pagar = round(sum(restos_pagar['saldo_inicial_nao_processados_inscritos_ultimo_ano']), 2)
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP NÃO PROCESSADOS INSCRITOS',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }


    def teste2(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '531200000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '531200000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_restos_pagar = round(sum(restos_pagar['saldo_inicial_nao_processados_inscritos_anos_anteriores']), 2)
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP NÃO PROCESSADOS - EXERCÍCIOS ANTERIORES',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste3(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '532100000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '532100000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_restos_pagar = round(sum(restos_pagar['saldo_inicial_processados_inscritos_ultimo_ano']), 2)
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP PROCESSADOS INSCRITOS',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste4(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '532200000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '532200000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_restos_pagar = round(sum(restos_pagar['saldo_inicial_processados_inscritos_anos_anteriores']), 2)
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP PROCESSADOS - EXERCÍCIOS ANTERIORES',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste5(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '631100000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '631100000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_restos_pagar = round(sum(restos_pagar['a_liquidar_nao_processados']), 2)
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP NÃO PROCESSADOS A LIQUIDAR',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste6(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '631300000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '631300000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_restos_pagar = round(sum(restos_pagar['liquidado_a_pagar_nao_processados']), 2)
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP NÃO PROCESSADOS LIQUIDADOS A PAGAR',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste7(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '631400000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '631400000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_restos_pagar = round(sum(restos_pagar['pagamento_nao_processados']), 2)
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP NÃO PROCESSADOS PAGOS',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste8(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'].str.startswith('6319'))
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'].str.startswith('6319'))
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_restos_pagar = round(sum(restos_pagar['cancelamento_nao_processados']), 2)
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP NÃO PROCESSADOS CANCELADOS',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste9(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '632100000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '632100000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_restos_pagar = round(sum(restos_pagar['saldo_final_processados']), 2)
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP PROCESSADOS A PAGAR',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste10(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '632200000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '632200000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_restos_pagar = round(sum(restos_pagar['pagamento_processados']), 2)
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP PROCESSADOS PAGOS',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste11(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'].str.startswith('6329'))
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'].str.startswith('6329'))
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_restos_pagar = round(sum(restos_pagar['cancelamento_processados']), 2)
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP PROCESSADOS CANCELADOS',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste12(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '632700000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '632700000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_restos_pagar = 0.0
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP PROCESSADOS - INSCRIÇÃO NO EXERCÍCIO',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste13(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '631710000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '631710000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_c - saldo_msc_d

        saldo_restos_pagar = 0.0
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP NÃO PROCESSADOS A LIQUIDAR - INSCRIÇÃO NO EXERCÍCIO',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste14(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '532700000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '532700000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_restos_pagar = 0.0
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP NÃO PROCESSADOS - INSCRIÇÃO NO EXERCÍCIO',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }

    def teste15(self, msc, restos_pagar):
        saldo_msc_d = round(sum(msc[
                                    (msc['ContaContabil'] == '531700000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'D')
                                    ]['Valor']), 2)
        saldo_msc_c = round(sum(msc[
                                    (msc['ContaContabil'] == '531700000')
                                    & (msc['TipoValor'] == 'ending_balance')
                                    & (msc['NaturezaValor'] == 'C')
                                    ]['Valor']), 2)
        saldo_msc = saldo_msc_d - saldo_msc_c

        saldo_restos_pagar = 0.0
        diff = round(saldo_msc - saldo_restos_pagar, 2)
        # print(f'\t{saldo_msc_d}D', f'{saldo_msc_c}C', f'MSC: {saldo_msc}', f'PAD: {saldo_restos_pagar}', f'DIF: {diff}')
        return {
            'teste': 'RP NÃO PROCESSADOS - INSCRIÇÃO NO EXERCÍCIO',
            'valor_msc': saldo_msc,
            'valor_restos_pagar': saldo_restos_pagar,
            'diff': diff
        }