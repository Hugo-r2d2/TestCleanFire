from django.conf import settings
from django.http import JsonResponse
from .utils import importar_dados_csv
from rest_framework.decorators import api_view
from .serializers import MunicipioQueimadaSerializer
from .models import MunicipioQueimada
import pandas as pd
import boto3
import time

# Função para conectar ao DynamoDB
def conectar_dynamodb():
    return boto3.resource(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

# Função para inserir dados no DynamoDB
def inserir_dados_no_dynamodb(df):
    dynamodb = conectar_dynamodb()
    table = dynamodb.Table('Queimadas')

    # Ordenar DataFrame pelo campo ID
    df = df.sort_values(by='ID')

    with table.batch_writer() as batch:
        for index, row in df.iterrows():
            item = {
                'ID': str(row['ID']),
                'Estado': row['Estado'],
                'Municipio': row['Municipio'],
                'DataHora': row['DataHora'].isoformat(),  # Usando DataHora como chave de classificação
                'Bioma': row['Bioma'],
                'Latitude': str(row['Latitude']),
                'Longitude': str(row['Longitude']),
                'FRP': str(row['FRP']),
                'Precipita': str(row['Precipitacao']) if not pd.isnull(row['Precipitacao']) else None,
                'DiasSemChuva': str(row['DiaSemChuva']),
            }
            batch.put_item(Item=item)

            # Pausa para não ultrapassar o throughput
            if index % 25 == 0:
                time.sleep(2)

# Função para processar o CSV e inserir os dados
def processar_csv_e_inserir_dados(request):
    caminho_csv = 'C:/Users/ihugo/OneDrive/Documentos/Repositorios/Python_Repo/TestClean/firedata/data/queimadas20232024.csv'

    try:
        # Importar os dados do CSV
        df = importar_dados_csv(caminho_csv)

        # Inserir os dados no DynamoDB
        inserir_dados_no_dynamodb(df)
        
        return JsonResponse({'status': 'Sucesso', 'mensagem': 'Dados inseridos com sucesso no DynamoDB'})
    
    except Exception as e:
        return JsonResponse({'status': 'Erro', 'mensagem': str(e)})

# views.py
# views.py
@api_view(['GET'])
def listar_dados_dynamodb(request):
    dynamodb = conectar_dynamodb()
    table = dynamodb.Table('Queimadas')

    response = table.scan()
    items = response.get('Items', [])

    # Ajustar o formato dos itens para o serializer
    dados_convertidos = []
    for item in items:
        dados_convertidos.append({
            'ID': item.get('ID'),  # Mapeia 'ID' para 'id'
            'Estado': item.get('Estado'),
            'Municipio': item.get('Municipio'),
            'DataHora': item.get('DataHora'),
            'Bioma': item.get('Bioma'),
            'Latitude': item.get('Latitude'),
            'Longitude': item.get('Longitude'),
            'FRP': item.get('FRP'),
            'Precipita': item.get('Precipita'),
            'DiasSemChuva': item.get('DiasSemChuva')
        })

    serializer = MunicipioQueimadaSerializer(dados_convertidos, many=True)
    return JsonResponse(serializer.data, safe=False)

