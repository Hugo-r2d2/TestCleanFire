# firedata/tests.py
import boto3
from django.conf import settings
from django.test import TestCase

class DynamoDBTestCase(TestCase):
    def test_conexao_dynamodb(self):
        try:
            dynamodb = boto3.resource(
                'dynamodb',
                region_name='us-east-1',
            )
            # Lista as tabelas no DynamoDB
            tabelas = list(dynamodb.tables.all())
            self.assertIsNotNone(tabelas)  # Verifica se a lista de tabelas não é vazia
        except Exception as e:
            self.fail(f'Erro na conexão com o DynamoDB: {str(e)}')
