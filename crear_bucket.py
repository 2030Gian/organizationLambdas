import boto3
import json

def lambda_handler(event, context):
    try:
        # Parsear el cuerpo JSON del evento
        body = json.loads(event['body'])
        nombre_bucket = body['nombre_bucket']

        s3 = boto3.client('s3')

        # Crear el bucket
        s3.create_bucket(Bucket=nombre_bucket)

        return {
            'statusCode': 200,
            'body': json.dumps(f'Bucket "{nombre_bucket}" creado exitosamente.')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al crear el bucket: {str(e)}')
        }