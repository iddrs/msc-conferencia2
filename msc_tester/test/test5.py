"""
Testa se os saldos e movimentação da MSC atual possui correspondência no BAL_VER.

Considera apenas o Código da Conta Contábil.

"""
import pandas as pd
from tqdm import tqdm


class Test:
    def __init__(self, app):
        self.name = 'valores_balver_msc'
        self.app = app

    def run(self):
        self.app.logger.debug('Preparando MSC...')
        msc = self.prepare_msc(self.app.msc_atual)

        self.app.logger.debug('Realizando o teste...')
        result = self.run_test(msc, self.app.balver)
        self.app.logger.debug('Devolvendo o resultado...')
        return result

    def run_test(self, msc, balver):
        result = []
        total = len(balver)
        with tqdm(total=total) as progressbar:
            for i, r in balver.iterrows():
                chave = r['conta_contabil']
                pad_saldo_inicial = r['saldo_inicial_chave_pad']
                pad_movimento_devedor = r['movimento_devedor_pad']
                pad_movimento_credor = r['movimento_credor_pad']
                pad_saldo_final = r['saldo_final_chave_pad']

                r_msc = msc[msc['conta_contabil'] == chave]
                if r_msc.empty:
                    msc_cc = ''
                    msc_saldo_inicial = ''
                    msc_movimento_devedor = ''
                    msc_movimento_credor = ''
                    msc_saldo_final = ''
                else:
                    msc_cc = r_msc['conta_contabil'].iloc[0]
                    msc_saldo_inicial = r_msc['saldo_inicial_chave_msc'].iloc[0]
                    msc_movimento_devedor = r_msc['movimento_devedor_msc'].iloc[0]
                    msc_movimento_credor = r_msc['movimento_credor_msc'].iloc[0]
                    msc_saldo_final = r_msc['saldo_final_chave_msc'].iloc[0]
                diff = False
                if pad_saldo_inicial != msc_saldo_inicial:
                    diff_saldo_inicial = True
                    diff = True
                else:
                    diff_saldo_inicial = False
                if pad_movimento_devedor != msc_movimento_devedor:
                    diff_movimento_devedor = True
                    diff = True
                else:
                    diff_movimento_devedor = False
                if pad_movimento_credor != msc_movimento_credor:
                    diff_movimento_credor = True
                    diff = True
                else:
                    diff_movimento_credor = False
                if pad_saldo_final != msc_saldo_final:
                    diff_saldo_final = True
                    diff = True
                else:
                    diff_saldo_final = False
                registro = {
                    'conta_contabil': chave,
                    'pad_saldo_inicial': pad_saldo_inicial,
                    'msc_saldo_inicial': msc_saldo_inicial,
                    'pad_movimento_devedor': pad_movimento_devedor,
                    'msc_movimento_devedor': msc_movimento_devedor,
                    'pad_movimento_credor': pad_movimento_credor,
                    'msc_movimento_credor': msc_movimento_credor,
                    'pad_saldo_final': pad_saldo_final,
                    'msc_saldo_final': msc_saldo_final,
                    'diff_saldo_inicial': diff_saldo_inicial,
                    'diff_movimento_devedor': diff_movimento_devedor,
                    'diff_movimento_credor': diff_movimento_credor,
                    'diff_saldo_final': diff_saldo_final,
                    'diff': diff
                }
                result.append(registro)
                progressbar.update(1)
        df = pd.DataFrame(result)
        df = df.loc[df['diff']]
        return df

    def prepare_msc(self, msc):
        msc = msc[['ContaContabil', 'Valor', 'TipoValor', 'NaturezaValor']]
        msc = msc.groupby(by=['ContaContabil', 'TipoValor', 'NaturezaValor'], as_index=False).sum()

        lista_cc = msc['ContaContabil'].unique()
        balancete = []
        for cc in lista_cc:
            saldo_inicial_devedor = round(sum(msc[
                                                  (msc['ContaContabil'] == cc)
                                                  & (msc['TipoValor'] == 'beginning_balance')
                                                  & (msc['NaturezaValor'] == 'D')
                                                  ]['Valor']), 2)
            saldo_inicial_credor = round(sum(msc[
                                                  (msc['ContaContabil'] == cc)
                                                  & (msc['TipoValor'] == 'beginning_balance')
                                                  & (msc['NaturezaValor'] == 'C')
                                                  ]['Valor']), 2)
            movimento_devedor = round(sum(msc[
                                                  (msc['ContaContabil'] == cc)
                                                  & (msc['TipoValor'] == 'period_change')
                                                  & (msc['NaturezaValor'] == 'D')
                                                  ]['Valor']), 2)
            movimento_credor = round(sum(msc[
                                              (msc['ContaContabil'] == cc)
                                              & (msc['TipoValor'] == 'period_change')
                                              & (msc['NaturezaValor'] == 'C')
                                              ]['Valor']), 2)
            saldo_final_devedor = round(sum(msc[
                                                  (msc['ContaContabil'] == cc)
                                                  & (msc['TipoValor'] == 'ending_balance')
                                                  & (msc['NaturezaValor'] == 'D')
                                                  ]['Valor']), 2)
            saldo_final_credor = round(sum(msc[
                                                (msc['ContaContabil'] == cc)
                                                & (msc['TipoValor'] == 'ending_balance')
                                                & (msc['NaturezaValor'] == 'C')
                                                ]['Valor']), 2)
            if saldo_inicial_devedor > saldo_inicial_credor:
                saldo_inicial = round(saldo_inicial_devedor - saldo_inicial_credor, 2)
                natureza_inicial = 'D'
            elif saldo_inicial_credor > saldo_inicial_devedor:
                saldo_inicial = round(saldo_inicial_credor - saldo_inicial_devedor, 2)
                natureza_inicial = 'C'
            else:
                saldo_inicial = 0.0
                natureza_inicial = ' '
            if saldo_final_devedor > saldo_final_credor:
                saldo_final = round(saldo_final_devedor - saldo_final_credor, 2)
                natureza_final = 'D'
            elif saldo_final_credor > saldo_final_devedor:
                saldo_final = round(saldo_final_credor - saldo_final_devedor, 2)
                natureza_final = 'C'
            else:
                saldo_final = 0.0
                natureza_final = ' '
            balancete.append({
                'conta_contabil': cc,
                'saldo_inicial_valor_msc': saldo_inicial,
                'saldo_inicial_natureza_msc': natureza_inicial,
                'movimento_devedor_msc': movimento_devedor,
                'movimento_credor_msc': movimento_credor,
                'saldo_final_valor_msc': saldo_final,
                'saldo_final_natureza_msc': natureza_final
            })

        df = pd.DataFrame(balancete)
        df['saldo_inicial_chave_msc'] = df['saldo_inicial_valor_msc'].astype(str) + df.saldo_inicial_natureza_msc
        df['saldo_final_chave_msc'] = df['saldo_final_valor_msc'].astype(str) + df.saldo_final_natureza_msc
        return df