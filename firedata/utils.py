# firedata/utils.py
import pandas as pd

def importar_dados_csv(caminho_csv):
    try:
        df = pd.read_csv(caminho_csv, encoding='ISO-8859-1')
        print("DataFrame importado:")
        print(df.head())  # Exibe as primeiras linhas do DataFrame
        df['DataHora'] = pd.to_datetime(df['DataHora'], errors='coerce')  # Corrigido para usar 'DataHora'
        return df
    except Exception as e:
        print(f"Erro ao importar o CSV: {e}")
        return None
