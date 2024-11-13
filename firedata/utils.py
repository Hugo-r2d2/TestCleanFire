import pandas as pd

def importar_dados_csv(caminho_csv):
    try:
        # Corrigir o delimitador e garantir que o formato de data seja interpretado corretamente
        df = pd.read_csv(caminho_csv, encoding='ISO-8859-1', delimiter=';')
        print("DataFrame importado:")
        print(df.head())  # Exibe as primeiras linhas do DataFrame
        
        # Converter a coluna 'DataHora' para datetime, tratando o formato brasileiro
        df['DataHora'] = pd.to_datetime(df['DataHora'], format='%d/%m/%Y', errors='coerce', dayfirst=True)
        
        # Verificar se a conversão foi bem-sucedida
        if df['DataHora'].isnull().any():
            print("Atenção: Algumas datas não foram convertidas corretamente.")
        
        return df
    except Exception as e:
        print(f"Erro ao importar o CSV: {e}")
        return None
