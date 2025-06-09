import boto3
import json
import base64 # Requerido para manejar contenido de archivo codificado en base64

def lambda_handler(event, context):
    try:
        # Parsear el cuerpo JSON del evento
        # Cuando se envían datos binarios a través de API Gateway, a menudo están codificados en base64.
        # El flag 'isBase64Encoded' en el evento puede indicar si está codificado.
        # Para simplificar, asumimos que 'file_content' estará codificado en base64.
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(event['body']).decode('utf-8')
        else:
            body = event['body']

        data = json.loads(body)

        nombre_bucket = data['nombre_bucket']
        ruta_archivo_en_s3 = data['ruta_archivo_en_s3'] # ej. "mi_directorio/mi_archivo.txt"
        contenido_archivo_base64 = data['contenido_archivo_base64'] # Contenido codificado en Base64

        s3 = boto3.client('s3')

        # Decodificar el contenido base64
        file_content = base64.b64decode(contenido_archivo_base64)

        # Subir el archivo
        s3.put_object(Bucket=nombre_bucket, Key=ruta_archivo_en_s3, Body=file_content)

        return {
            'statusCode': 200,
            'body': json.dumps(f'Archivo subido exitosamente a s3://{nombre_bucket}/{ruta_archivo_en_s3}')
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Parámetro faltante: {str(e)}. Por favor, proporcione nombre_bucket, ruta_archivo_en_s3, y contenido_archivo_base64.')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al subir el archivo: {str(e)}')
        }