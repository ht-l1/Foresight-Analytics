import pandas as pd

class DataLoader:
    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path)
        df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
        return df
    
    @staticmethod
    def filter_by_department(df: pd.DataFrame, department: str) -> pd.DataFrame:
        return df[df['Department'] == department]