import boto3
import json

def lambda_handler(event, context):
    try:
        # --- CORRECCIÓN AQUÍ ---
        if isinstance(event.get('body'), dict):
            body_data = event['body']
        else:
            body_data = json.loads(event.get('body', '{}'))
        # --- FIN DE LA CORRECCIÓN ---

        nombre_bucket = body_data['nombre_bucket']
        nombre_directorio = body_data['nombre_directorio']

        s3 = boto3.client('s3')

        # S3 no tiene directorios en el sentido tradicional.
        # Creamos un objeto vacío con una barra al final para simular un directorio.
        object_key = f'{nombre_directorio}/'
        s3.put_object(Bucket=nombre_bucket, Key=object_key)

        return {
            'statusCode': 200,
            'body': json.dumps(f'Directorio "{nombre_directorio}" creado exitosamente en el bucket "{nombre_bucket}".')
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Parámetro faltante: {str(e)}. Asegúrate de enviar "nombre_bucket" y "nombre_directorio" en el cuerpo JSON.')
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Formato JSON inválido en el cuerpo de la solicitud.')
        }
    except s3.exceptions.NoSuchBucket:
        return {
            'statusCode': 404,
            'body': json.dumps(f'El bucket "{nombre_bucket}" no existe.')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al crear el directorio: {str(e)}')
        }