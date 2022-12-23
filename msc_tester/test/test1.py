"""
Testa se o valor do saldo final da MSC anterior é igual ao valor do saldo inicial da MSC atual.

Considera a conta contábil qualificada, ou seja, o código da conta contábil + informações complementares
"""
import pandas as pd
from tqdm import tqdm


class Test:
    def __init__(self, app):
        self.name = 'msc_anterior_atual_saldos'
        self.app = app

    def run(self):
        self.app.logger.debug('Preparando as coisas... Isso pode demorar um pouco (e eu não tenho ideia de quanto pode demorar.)')
        msc_anterior = self.app.msc_anterior.copy()
        msc_anterior = self.filtra_ending_balance(msc_anterior)
        msc_anterior = self.filtra_com_saldo_final(msc_anterior)
        msc_anterior = self.cria_chave(msc_anterior)
        msc_anterior = self.agrupa_saldos(msc_anterior)

        msc_atual = self.app.msc_atual.copy()
        msc_atual = self.filtra_beginning_balance(msc_atual)
        msc_atual = self.cria_chave(msc_atual)
        msc_atual = self.agrupa_saldos(msc_atual)

        self.app.logger.debug('Realizando o teste...')
        resultado = self.compara_anterior_atual(msc_anterior, msc_atual)

        self.app.logger.debug('Devolvendo o resultado...')
        df = pd.DataFrame.from_dict(resultado)
        return df

    def agrupa_saldos(self, msc):
        chaves = msc['Chave'].unique()
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
            saldos.append(str(saldo))
            naturezas.append(natureza)

        contas = msc[['Chave', 'ContaContabil', 'PO', 'FP', 'DC', 'FR', 'CO', 'NR', 'ND', 'FS', 'AI']].drop_duplicates()
        contas['Saldo'] = saldos
        contas['Natureza'] = naturezas
        contas = contas[contas['Saldo'] != '0.0']
        contas['SaldoComparavel'] = contas.Saldo + contas.Natureza
        return contas

    def compara_anterior_atual(self, msc_anterior, msc_atual):
        resultado = []
        msc0 = msc_anterior.copy()
        msc1 = msc_atual.copy()

        total = len(msc0)

        with tqdm(total=total) as progressbar:
            for i, anterior in msc0.iterrows():
                chave = anterior['Chave']
                atual = msc1[msc1['Chave'] == chave]
                vl_anterior = anterior['SaldoComparavel']
                vl_atual = atual['SaldoComparavel']
                if len(vl_anterior) == 0:
                    vl_anterior = ''
                if len(vl_atual) == 0:
                    vl_atual = ''
                if type(vl_anterior) is not str:
                    vl_anterior = vl_anterior[0]
                if type(vl_atual) is not str:
                    vl_atual = vl_atual[0]
                if vl_anterior == vl_atual:
                    pass
                else:
                    resultado.append({
                        'ContaContabil': anterior['ContaContabil'],
                        'PO': anterior['PO'],
                        'FP': anterior['FP'],
                        'DC': anterior['DC'],
                        'FR': anterior['FR'],
                        'CO': anterior['CO'],
                        'NR': anterior['NR'],
                        'ND': anterior['ND'],
                        'FS': anterior['FS'],
                        'AI': anterior['AI'],
                        'SaldoFinalAnterior': float(vl_anterior[:-1].zfill(1)),
                        'NaturezaAnterior': vl_anterior.rjust(1, ' ')[-1],
                        'SaldoInicialAtual': float(vl_atual[:-1].zfill(1)),
                        'NaturezaAtual': vl_atual.rjust(1, ' ')[-1]
                    })
                progressbar.update(1)

        return resultado

    def cria_chave(self, msc):
        msc['Chave'] = msc.ContaContabil.fillna('') + '_PO:' + msc.PO.fillna('') + '_FP:' + msc.FP.fillna('') + '_DC:' + msc.DC.fillna('') + '_FR:' + msc.FR.fillna('') + '_CO:' + msc.CO.fillna('') + '_NR:' + msc.NR.fillna('') + '_ND:' + msc.ND.fillna('') + '_FS:' + msc.FS.fillna('') + '_AI:' + msc.AI.fillna('')
        return msc

    def filtra_beginning_balance(self, msc_atual):
        return msc_atual[msc_atual['TipoValor'] == 'beginning_balance']

    def filtra_ending_balance(self, msc_anterior):
        return msc_anterior[msc_anterior['TipoValor'] == 'ending_balance']

    def filtra_com_saldo_final(self, msc_anterior):
        return msc_anterior[msc_anterior['Valor'] > 0]