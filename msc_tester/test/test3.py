"""
Verifica se as contas do BAL_VER estão na MSC.

Considera apenas o Código da Conta Contábil.

"""
import pandas as pd
from tqdm import tqdm


class Test:
    def __init__(self, app):
        self.name = 'contas_balver_msc'
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
        total = len(balver)
        with tqdm(total=total) as progressbar:
            for i, r in balver.iterrows():
                chave = r['conta_contabil_mapeada']
                if chave in msc:
                    cc_msc = chave
                else:
                    cc_msc = None
                registro = {
                    'conta_contabil_mapeada': chave,
                    'conta_contabil_pad': r['conta_contabil_pad'],
                    'conta_contabil_msc': cc_msc
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
        for i, r in df.iterrows():
            if self.app.balver['conta_contabil'].isin([r['conta_contabil_mapeada']]).any():
                continue
            else:
                df = df.drop(i)
        return df