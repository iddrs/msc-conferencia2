"""
Verifica se as contas da MSC estão no BAL_VER.

Considera apenas o Código da Conta Contábil.

"""
import pandas as pd
from tqdm import tqdm


class Test:
    def __init__(self, app):
        self.name = 'contas_msc_balver'
        self.app = app

    def run(self):
        self.app.logger.debug('Preparando MSC...')
        msc = self.prepare_msc(self.app.msc_atual.copy())
        balver = self.prepare_balver(self.app.balver_atual.copy())
        self.app.logger.debug('Realizando o teste...')
        result = self.run_test(msc, balver)
        self.app.logger.debug('Devolvendo o resultado...')
        return result

    def run_test(self, msc, balver):
        result = []
        total = len(msc)
        with tqdm(total=total) as progressbar:
            for chave in msc:
                if balver['conta_contabil_mapeada'].isin([chave]).any():
                    cc_balver = balver[balver['conta_contabil_mapeada'] == chave]['conta_contabil_pad'].iloc[0]
                else:
                    cc_balver = None
                registro = {
                    'conta_contabil_mapeada': chave,
                    'conta_contabil_pad': cc_balver,
                    'conta_contabil_msc': chave
                }
                result.append(registro)
                progressbar.update(1)
        df = pd.DataFrame(result)
        df = df.loc[df['conta_contabil_pad'].isnull()]
        return df

    def prepare_msc(self, msc):
        cc = msc['ContaContabil']
        cc = cc.unique()
        return cc

    def prepare_balver(self, balver):
        balver = balver[balver['escrituracao'] == 'S']
        cc = balver['conta_contabil']
        cc = cc.unique()
        mapeamento = self.app.busca_mapeamento(cc)
        df = pd.DataFrame({'conta_contabil_mapeada': mapeamento, 'conta_contabil_pad': cc})
        # for i, r in df.iterrows():
        #     if self.app.balver['conta_contabil'].isin([r['conta_contabil_mapeada']]).any():
        #         continue
        #     else:
        #         df = df.drop(i)
        return df
