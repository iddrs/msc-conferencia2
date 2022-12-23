import pandas as pd

class ExcelReporter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}

    def write(self, df, test_name):
        self.data[test_name] = df

    def save(self):
        with pd.ExcelWriter(self.file_path) as writer:
            for test_name, df in self.data.items():
                df.to_excel(writer, sheet_name=test_name, index=False)