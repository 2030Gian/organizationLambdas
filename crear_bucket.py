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

        s3 = boto3.client('s3')

        # Crear el bucket
        s3.create_bucket(Bucket=nombre_bucket)

        return {
            'statusCode': 200,
            'body': json.dumps(f'Bucket "{nombre_bucket}" creado exitosamente.')
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Parámetro faltante: {str(e)}. Asegúrate de enviar "nombre_bucket" en el cuerpo JSON.')
        }
    except s3.exceptions.BucketAlreadyOwnedByYou:
        return {
            'statusCode': 409, # Conflict
            'body': json.dumps(f'El bucket "{nombre_bucket}" ya existe y es de tu propiedad.')
        }
    except s3.exceptions.BucketAlreadyExists:
        return {
            'statusCode': 409, # Conflict
            'body': json.dumps(f'El bucket "{nombre_bucket}" ya existe y es propiedad de otra cuenta.')
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Formato JSON inválido en el cuerpo de la solicitud.')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al crear el bucket: {str(e)}')
        }