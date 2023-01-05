"""
Controlador geral da aplicação.
"""
import sqlite3

import pandas as pd


class App:
    def __init__(self, logger, reporter, mapeamento_cc, msc_atual, msc_anterior, balver_atual, balver_anterior, balrec, testes):
        self.logger = logger
        self.reporter = reporter
        self.mapeamento_cc = mapeamento_cc
        self.msc_anterior = msc_anterior
        self.msc_atual = msc_atual
        self.balver_atual = balver_atual
        self.balver_anterior = balver_anterior
        self.balrec = balrec
        self.testes = testes


    def run(self):
        self.logger.info('Preparando BAL_VER...')
        self.balver = self.prepare_balver(self.balver_anterior, self.balver_atual)

        self.logger.info('Execução dos testes iniciada...')

        for t in self.testes:
            test = t.Test(app=self)
            self.logger.info(f'Executando teste {test.name}...')
            result = test.run()
            self.reporter.write(result, test.name)
        self.reporter.save()

    def prepare_balver(self, balver_anterior, balver_atual):
        # cria uma lista com as contas contábeis
        anterior = balver_anterior[balver_anterior['escrituracao'] == 'S']
        atual = balver_atual[balver_atual['escrituracao'] == 'S']
        lista_cc = pd.concat([anterior['conta_contabil'], atual['conta_contabil']])
        lista_cc = lista_cc.unique()

        # monta o balancete mensal
        balancete = []
        for cc in lista_cc:
            # saldo inicial
            saldo_inicial_devedor = sum(balver_anterior[balver_anterior['conta_contabil'] == cc]['saldo_atual_devedor'])
            saldo_inicial_credor = sum(balver_anterior[balver_anterior['conta_contabil'] == cc]['saldo_atual_credor'])
            if saldo_inicial_devedor > saldo_inicial_credor:
                saldo_inicial = round(saldo_inicial_devedor - saldo_inicial_credor, 2)
                natureza_inicial = 'D'
            elif saldo_inicial_credor > saldo_inicial_devedor:
                saldo_inicial = round(saldo_inicial_credor - saldo_inicial_devedor, 2)
                natureza_inicial = 'C'
            else:
                saldo_inicial = 0.0
                natureza_inicial = ' '

            # movimentação a débito
            movimento_devedor_anterior = sum(balver_anterior[balver_anterior['conta_contabil'] == cc]['movimento_devedor'])
            movimento_credor_anterior = sum(balver_anterior[balver_anterior['conta_contabil'] == cc]['movimento_credor'])
            movimento_devedor_atual = sum(balver_atual[balver_atual['conta_contabil'] == cc]['movimento_devedor'])
            movimento_credor_atual = sum(balver_atual[balver_atual['conta_contabil'] == cc]['movimento_credor'])
            movimento_devedor = round(movimento_devedor_atual - movimento_devedor_anterior, 2)
            movimento_credor = round(movimento_credor_atual - movimento_credor_anterior, 2)

            # saldo final
            saldo_final_devedor = sum(balver_atual[balver_atual['conta_contabil'] == cc]['saldo_atual_devedor'])
            saldo_final_credor = sum(balver_atual[balver_atual['conta_contabil'] == cc]['saldo_atual_credor'])
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
                'saldo_inicial_valor': saldo_inicial,
                'saldo_inicial_natureza': natureza_inicial,
                'movimento_devedor': movimento_devedor,
                'movimento_credor': movimento_credor,
                'saldo_final_valor': saldo_final,
                'saldo_final_natureza': natureza_final
            })
        df = pd.DataFrame(balancete)
        df = df.loc[
            (df['saldo_inicial_valor'] > 0)
            | (df['saldo_final_valor'] > 0)
            | (df['movimento_devedor'] > 0)
            | (df['movimento_credor'] > 0)
        ]
        df['conta_contabil'] = self.busca_mapeamento(df['conta_contabil'].copy())
        df = df.groupby(['conta_contabil', 'saldo_inicial_natureza', 'saldo_final_natureza'], as_index=False).sum()
        df.columns = ['conta_contabil', 'saldo_inicial_natureza_pad', 'saldo_final_natureza_pad',
       'saldo_inicial_valor_pad', 'movimento_devedor_pad', 'movimento_credor_pad',
       'saldo_final_valor_pad']
        df['saldo_inicial_chave_pad'] = df['saldo_inicial_valor_pad'].astype(str) + df.saldo_inicial_natureza_pad
        df['saldo_final_chave_pad'] = df['saldo_final_valor_pad'].astype(str) + df.saldo_final_natureza_pad

        return df

    def busca_mapeamento(self, list_cc):
        lista = []
        for cc_pad in list_cc:
            if self.mapeamento_cc['cc_pad'].isin([cc_pad]).any():
                index = self.mapeamento_cc.loc[self.mapeamento_cc['cc_pad'] == cc_pad].index[0]
                lista.append(self.mapeamento_cc.at[index, 'cc_msc'])
            else:
                lista.append(cc_pad[0:9])
        return lista