"""
Testa se o saldo inicial com a movimentação corresponde ao saldo final

Considera a conta contábil qualificada, ou seja, o código da conta contábil + informações complementares
"""
import pandas as pd
from tqdm import tqdm


class Test:
    def __init__(self, app):
        self.name = 'msc_diferenca_saldo_final'
        self.app = app

    def run(self):
        self.app.logger.debug(
            'Preparando as coisas... Isso pode demorar um pouco (e eu não tenho ideia de quanto pode demorar.)')
        msc_atual = self.app.msc_atual.copy()
        # msc_atual = self.filtra_beginning_balance(msc_atual)
        chaves = self.cria_chave(msc_atual)
        contas = self.agrupa_saldos(chaves)
        # print(msc_atual)
        # msc_atual.to_excel('teste.xlsx')
        # exit()

        self.app.logger.debug('Realizando o teste...')
        resultado = self.testa(msc_atual, contas)

        self.app.logger.debug('Devolvendo o resultado...')
        df = pd.DataFrame.from_dict(resultado)
        return df

    def agrupa_saldos(self, msc_atual):
        chaves = msc_atual['Chave'].unique()
        contas = msc_atual[['Chave', 'ContaContabil', 'PO', 'FP', 'DC', 'FR', 'CO', 'NR', 'ND', 'FS', 'AI']].drop_duplicates()

        # saldo inicial
        msc = self.filtra_beginning_balance(msc_atual)
        saldos = []
        naturezas = []
        for c in chaves:
            saldo_devedor = round(sum(msc[(msc['Chave'] == c) & (msc['NaturezaValor'] == 'D')]['Valor']), 2)
            saldo_credor = round(sum(msc[(msc['Chave'] == c) & (msc['NaturezaValor'] == 'C')]['Valor']), 2)
            if not callable(getattr(saldo_devedor, '__iter__', None)):
                saldo_devedor = [saldo_devedor]
            if not callable(getattr(saldo_credor, '__iter__', None)):
                saldo_credor = [saldo_credor]
            saldo_devedor = round(sum(saldo_devedor), 2)
            saldo_credor = round(sum(saldo_credor), 2)
            if saldo_devedor > saldo_credor:
                saldo = round(saldo_devedor - saldo_credor, 2)
                natureza = 'D'
            elif saldo_credor > saldo_devedor:
                saldo = round(saldo_credor - saldo_devedor, 2)
                natureza = 'C'
            else:
                saldo = 0.0
                natureza = None
            saldos.append(saldo)
            naturezas.append(natureza)
        contas['saldo_inicial_valor'] = saldos
        contas['saldo_inicial_natureza'] = naturezas

        # saldo final
        msc = self.filtra_ending_balance(msc_atual)
        saldos = []
        naturezas = []
        for c in chaves:
            saldo_devedor = round(sum(msc[(msc['Chave'] == c) & (msc['NaturezaValor'] == 'D')]['Valor']), 2)
            saldo_credor = round(sum(msc[(msc['Chave'] == c) & (msc['NaturezaValor'] == 'C')]['Valor']), 2)
            if not callable(getattr(saldo_devedor, '__iter__', None)):
                saldo_devedor = [saldo_devedor]
            if not callable(getattr(saldo_credor, '__iter__', None)):
                saldo_credor = [saldo_credor]
            saldo_devedor = round(sum(saldo_devedor), 2)
            saldo_credor = round(sum(saldo_credor), 2)
            if saldo_devedor > saldo_credor:
                saldo = round(saldo_devedor - saldo_credor, 2)
                natureza = 'D'
            elif saldo_credor > saldo_devedor:
                saldo = round(saldo_credor - saldo_devedor, 2)
                natureza = 'C'
            else:
                saldo = 0.0
                natureza = None
            saldos.append(saldo)
            naturezas.append(natureza)
        contas['saldo_final_valor'] = saldos
        contas['saldo_final_natureza'] = naturezas

        # movimento devedor
        msc = self.filtra_period_change(msc_atual)
        movimento = []
        for c in chaves:
            movimento_devedor = round(sum(msc[(msc['Chave'] == c) & (msc['NaturezaValor'] == 'D')]['Valor']), 2)
            movimento.append(movimento_devedor)
        contas['movimento_devedor'] = movimento

        # movimento credor
        msc = self.filtra_period_change(msc_atual)
        movimento = []
        for c in chaves:
            movimento_credor = round(sum(msc[(msc['Chave'] == c) & (msc['NaturezaValor'] == 'C')]['Valor']), 2)
            movimento.append(movimento_credor)
        contas['movimento_credor'] = movimento
        return contas

    def testa(self, msc_atual, contas):
        chaves = msc_atual['Chave'].unique()
        # saldo final calculado
        calculado = []
        diferenca = []
        for c in chaves:
            saldo_inicial = round(sum(contas[contas['Chave'] == c]['saldo_inicial_valor']), 2)
            natureza_inicial = contas[contas['Chave'] == c]['saldo_inicial_natureza']
            debitos = round(sum(contas[contas['Chave'] == c]['movimento_devedor']), 2)
            creditos = round(sum(contas[contas['Chave'] == c]['movimento_credor']), 2)
            saldo_final = round(sum(contas[contas['Chave'] == c]['saldo_final_valor']), 2)
            natureza_final = contas[contas['Chave'] == c]['saldo_final_natureza']
            if int(c[0:1]) % 2 == 0:
                tipo_conta = 'C'
            else:
                tipo_conta = 'D'
            if tipo_conta == 'D':
                if natureza_inicial[0] == 'C':
                    saldo_inicial = saldo_inicial * -1
                if natureza_final[0] == 'C':
                    saldo_final = saldo_final * -1
                saldo_calculado = saldo_inicial + debitos - creditos
                if round(saldo_calculado, 2) == round(saldo_final, 2):
                    diferenca.append(False)
                else:
                    diferenca.append(True)
                calculado.append(saldo_calculado)
            else:
                if natureza_inicial[0] == 'D':
                    saldo_inicial = saldo_inicial * -1
                if natureza_final[0] == 'D':
                    saldo_final = saldo_final * -1
                saldo_calculado = saldo_inicial - debitos + creditos
                if round(saldo_calculado, 2) == round(saldo_final, 2):
                    diferenca.append(False)
                else:
                    diferenca.append(True)
                calculado.append(saldo_calculado)
        contas['saldo_final_calculado'] = calculado
        contas['diferenca'] = diferenca
        contas = contas[contas['diferenca'] == True]

        return contas


    def cria_chave(self, msc):
        msc['Chave'] = msc.ContaContabil.fillna('') + '_PO:' + msc.PO.fillna('') + '_FP:' + msc.FP.fillna(
            '') + '_DC:' + msc.DC.fillna('') + '_FR:' + msc.FR.fillna('') + '_CO:' + msc.CO.fillna(
            '') + '_NR:' + msc.NR.fillna('') + '_ND:' + msc.ND.fillna('') + '_FS:' + msc.FS.fillna(
            '') + '_AI:' + msc.AI.fillna('')
        return msc

    def filtra_beginning_balance(self, msc_atual):
        return msc_atual[msc_atual['TipoValor'] == 'beginning_balance']

    def filtra_ending_balance(self, msc_atual):
        return msc_atual[msc_atual['TipoValor'] == 'ending_balance']

    def filtra_period_change(self, msc_atual):
        return msc_atual[msc_atual['TipoValor'] == 'period_change']
    #
    # def filtra_com_saldo_final(self, msc_anterior):
    #     return msc_anterior[msc_anterior['Valor'] > 0]