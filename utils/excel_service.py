import pandas as pd

class ExcelService:

    @staticmethod
    def read_excel(file_path: str):

        df = pd.read_excel(file_path)

        df = df.fillna("")

        return df

    @staticmethod
    def get_columns(df):

        return list(df.columns)

    @staticmethod
    def get_records(df):

        return df.to_dict("records")