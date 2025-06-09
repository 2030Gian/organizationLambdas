import boto3
import json

def lambda_handler(event, context):
    # Entrada (no se espera un cuerpo JSON para listar buckets)

    # Proceso
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    lista = []
    for bucket in response['Buckets']:
        lista.append(bucket["Name"])

    # Salida
    return {
        'statusCode': 200,
        'lista_buckets': lista
    }