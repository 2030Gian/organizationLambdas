import boto3
import json

def lambda_handler(event, context):
    try:
        # --- CORRECCIÓN AQUÍ ---
        # Verificamos si event['body'] ya es un diccionario (parseado por API Gateway)
        # o si es una cadena JSON que necesita ser parseada.
        if isinstance(event.get('body'), dict):
            body_data = event['body']
        else:
            # Si 'body' no existe o es None, usamos un diccionario vacío para evitar errores.
            # json.loads() espera una cadena, por eso usamos .get('', '{}')
            body_data = json.loads(event.get('body', '{}'))
        # --- FIN DE LA CORRECCIÓN ---

        # Ahora accedemos al nombre_bucket desde body_data
        nombre_bucket = body_data['bucket']

        # Proceso
        s3 = boto3.client('s3')
        # list_objects_v2 es más moderno y recomendado para listar objetos
        response = s3.list_objects_v2(Bucket=nombre_bucket)
        lista = []
        # Comprobamos si 'Contents' existe antes de iterar, por si el bucket está vacío
        if 'Contents' in response:
            for obj in response['Contents']:
                lista.append(obj['Key'])

        return {
            'statusCode': 200,
            'bucket': nombre_bucket,
            'lista_objetos': lista
        }
    except KeyError as e:
        # Si el campo 'bucket' no se encuentra en el body
        return {
            'statusCode': 400,
            'body': json.dumps(f'Parámetro faltante: {str(e)}. Asegúrate de enviar "bucket" en el cuerpo JSON.')
        }
    except json.JSONDecodeError:
        # Si el cuerpo no es un JSON válido
        return {
            'statusCode': 400,
            'body': json.dumps('Formato JSON inválido en el cuerpo de la solicitud.')
        }
    except s3.exceptions.NoSuchBucket:
        # Si el bucket no existe
        return {
            'statusCode': 404,
            'body': json.dumps(f'El bucket "{nombre_bucket}" no existe.')
        }
    except Exception as e:
        # Captura cualquier otra excepción
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al listar objetos del bucket: {str(e)}')
        }