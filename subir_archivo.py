import boto3
import json
import base64

def lambda_handler(event, context):
    try:
        # --- CORRECCIÓN AQUÍ ---
        raw_body = event.get('body')
        data = {}

        # Si el cuerpo ya es un diccionario (API Gateway lo parseó), lo usamos directamente.
        if isinstance(raw_body, dict):
            data = raw_body
        else:
            # Si es una cadena y está codificado en base64, primero decodificamos el body entero
            # y luego parseamos el JSON resultante.
            if event.get('isBase64Encoded', False) and isinstance(raw_body, str):
                decoded_body_str = base64.b64decode(raw_body).decode('utf-8')
                data = json.loads(decoded_body_str)
            elif isinstance(raw_body, str): # Si es una cadena pero NO está base64, asumimos que es JSON directo
                data = json.loads(raw_body)
            else: # Si no es ni dict ni str, o es None, significa un cuerpo de solicitud problemático
                raise ValueError("El cuerpo de la solicitud no es un JSON válido o está vacío.")
        # --- FIN DE LA CORRECCIÓN ---

        nombre_bucket = data['nombre_bucket']
        ruta_archivo_en_s3 = data['ruta_archivo_en_s3'] # Ej: "mi_directorio/mi_archivo.txt"
        contenido_archivo_base64 = data['contenido_archivo_base64'] # Contenido del archivo en Base64

        s3 = boto3.client('s3')

        # Decodificar el contenido del archivo de Base64 a bytes
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
            'body': json.dumps(f'Parámetro faltante: {str(e)}. Por favor, proporcione "nombre_bucket", "ruta_archivo_en_s3", y "contenido_archivo_base64" en el cuerpo JSON.')
        }
    except (json.JSONDecodeError, ValueError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error en el formato JSON o Base64 del cuerpo: {str(e)}')
        }
    except s3.exceptions.NoSuchBucket:
        return {
            'statusCode': 404,
            'body': json.dumps(f'El bucket "{nombre_bucket}" no existe.')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error general al subir el archivo: {str(e)}')
        }