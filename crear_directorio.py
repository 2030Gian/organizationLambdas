import boto3
import json

def lambda_handler(event, context):
    try:
        # Parsear el cuerpo JSON del evento
        body = json.loads(event['body'])
        nombre_bucket = body['nombre_bucket']
        nombre_directorio = body['nombre_directorio']

        s3 = boto3.client('s3')

        # S3 no tiene directorios en el sentido tradicional.
        # Creamos un objeto vacío con una barra al final para simular un directorio.
        object_key = f'{nombre_directorio}/'
        s3.put_object(Bucket=nombre_bucket, Key=object_key)

        return {
            'statusCode': 200,
            'body': json.dumps(f'Directorio "{nombre_directorio}" creado exitosamente en el bucket "{nombre_bucket}".')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al crear el directorio: {str(e)}')
        }