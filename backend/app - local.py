# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 12:14:22 2024

@author: USUARIO
"""

####sevidor local
import random
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS  # Importa CORS
import pandas as pd
from datetime import datetime
import subprocess
from io import BytesIO


app = Flask(__name__, 
            static_folder='site/static',  # Configura la carpeta estática
            template_folder='site/templates')

CORS(app)  # Habilita CORS para todas las rutas

# Función para leer el archivo de credenciales y verificar si el correo existe
path_data_base = "C:/Users/USUARIO/Juan Carlos/Software San Francisco de Asis/pagina_web/consulta_automatica_procesos_judiciales/back_end/data_base"
path_df_token = os.path.join(path_data_base, "1token.txt")
path_df_credentials = os.path.join(path_data_base, "2credentials_db.txt")
path_df_ingreso = os.path.join(path_data_base, "5ingreso_plataforma.txt")
path_archivo_procesos_por_cliente = os.path.join(path_data_base, "3procesos_por_cliente.txt")

#def verificar_correo(mail_username):
#    
#    if os.path.exists(path_df_credentials):
#        with open(path_df_credentials , 'r') as f:
#            for line in f:
#                correo, _, _ = line.strip().split('|')
#                if correo == mail_username:
#                    return True
#    return False


def verificar_correo(mail_username):
    """
    Verifica si un correo electrónico está presente en la columna 'correo'
    de un archivo de texto con encabezados.

    Args:
        mail_username (str): El correo a verificar.
        path_df_credentials (str): Ruta al archivo de credenciales.

    Returns:
        bool: True si el correo está presente, False en caso contrario.
    """
    if os.path.exists(path_df_credentials):
        try:
            # Lee el archivo como un DataFrame con encabezados
            df = pd.read_csv(path_df_credentials, sep='|')
            
            # Verifica si la columna 'correo' existe y si el correo está en ella
            if 'correo' in df.columns:
                return mail_username in df['correo'].values
            else:
                print("La columna 'correo' no se encuentra en el archivo.")
                return False
        except Exception as e:
            print(f"Error al leer o procesar el archivo: {e}")
            return False
    else:
        print(f"Archivo no encontrado: {path_df_credentials}")
        return False


# Función para generar un código de verificación de 4 dígitos
def generar_codigo_verificacion(mail_username):
    codigo_email = str(random.randint(1000, 9999))

    # Abrir el archivo en modo lectura y escritura
    with open(path_df_token, 'r+') as file:
        lines = file.readlines()
        file.seek(0)  # Volver al inicio del archivo

        # Verificar si ya existe el correo en el archivo
        found = False
        for i, line in enumerate(lines):
            correo, token = line.strip().split('|')
            if correo == mail_username:
                # Si el correo ya existe, sobrescribir con el nuevo token
                lines[i] = f"{mail_username}|{codigo_email}\n"
                found = True
                break

        if not found:
            # Si el correo no se encontró, agregarlo al final del archivo
            lines.append(f"{mail_username}|{codigo_email}\n")

        # Escribir de nuevo todas las líneas en el archivo
        file.writelines(lines)

    return codigo_email
    

# Función para enviar el correo con el código
def enviar_correo(mail_username, codigo):
    sender_email = "datajuancahb@gmail.com"
    sender_password = "wuzx vwga fwev mkdq"
    receiver_email = mail_username

    # Crea el mensaje
    subject = "Código de verificación"
    body = f"Tu código de verificación es: {codigo}"


# Crear el mensaje con codificación UTF-8
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Configura el servidor SMTP de Gmail
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Función para manejar el registro de usuario
@app.route('/correo_registrar', methods=['POST'])
def correo_registrar():
    data = request.json
    mail_username = data.get('mail_username')
    password_sfa = data.get('password_sfa')
    
    print('Correo recibido:', mail_username)
    print('Contraseña recibida:', password_sfa)

    # Verifica si el correo ya está registrado
    if verificar_correo(mail_username):
        return jsonify({'mensaje': 'El correo ya está registrado. Intenta con otro correo.'})

    # Si no está registrado, generar código de verificación
    codigo = generar_codigo_verificacion(mail_username)
    print(codigo)
    # Enviar el código por correo
    enviar_correo(mail_username, codigo)
    
    # Solicitar al usuario que ingrese el código de verificación
    return jsonify({'mensaje': 'Correo enviado con el código de verificación. Por favor, ingresa el código de 4 dígitos enviado a tu correo.'})


def eliminar_token(correo, path_df_token):
    # Cargar el archivo token.txt en un DataFrame
    try:
        df_tokens = pd.read_csv(path_df_token, sep='|', header=None, names=['correo', 'codigo'])
    except FileNotFoundError:
        print('Archivo token.txt no encontrado.')
        return

    # Filtrar las filas que no contienen el correo que queremos eliminar
    df_tokens_filtrado = df_tokens[df_tokens['correo'] != correo]

    # Verificar si hay cambios (si no hay coincidencia, no se hace nada)
    if len(df_tokens_filtrado) == len(df_tokens):
        print("El correo no se encuentra en el archivo.")
        return

    # Sobrescribir el archivo token.txt con las filas filtradas
    df_tokens_filtrado.to_csv(path_df_token, sep='|', header=False, index=False)

    print(f"Token con correo {correo} eliminado correctamente.")

# Función para verificar el código ingresado

@app.route('/verificar_codigo', methods=['POST'])
def verificar_codigo():
    data = request.json
    mail_username = data.get('mail_username')
    password_sfa = data.get('password_sfa')
    codigo_ingresado = data.get('codigo_ingresado')
    fecha_hora_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    print('Correo recibido:', mail_username)
    print('Contraseña recibida:', password_sfa)
    print('Codigo ingresado:', codigo_ingresado)

    # Cargar el archivo token.txt en un DataFrame
    try:
        df_tokens = pd.read_csv(path_df_token, sep='|', header=None, names=['correo', 'codigo'])
    except FileNotFoundError:
        return jsonify({'mensaje': 'Archivo de tokens no encontrado.'})

    # Verificar si el correo y el código coinciden
    
    user_token = df_tokens[df_tokens['correo'] == mail_username]['codigo'].values

    if len(user_token) > 0 and str(user_token[0]) == str(codigo_ingresado):
        # Si el código es correcto, agregar el correo y la contraseña al archivo credentials_db.txt
        with open(path_df_credentials , 'a') as f:
            f.write(f'{mail_username}|{password_sfa}|{fecha_hora_registro}\n')
            
            #eliminar el código de tokens de ese usuario
            eliminar_token(correo = mail_username, path_df_token = path_df_token)
        return jsonify({'mensaje': 'Registro exitoso, puedes iniciar sesión ahora.'})
    
    # Si no se encuentra el correo o el código no coincide
    return jsonify({'mensaje': 'El código es incorrecto. Intenta nuevamente.'})
    #return jsonify({"token_enviado": "satisfactoriamente"})

@app.route('/login', methods=['POST'])
def correo_login():
    data = request.json
    mail_username = data.get('mail_username')
    password_sfa = data.get('password_sfa')
    # Obtener la fecha y hora actual en el formato deseado
    fecha_hora_ingreso = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    try:
        # Cargar los credenciales desde el archivo
        df_credentials = pd.read_csv(path_df_credentials, sep='|')

        # Verificar si existe un registro que coincida con correo y contraseña
        usuario_valido = df_credentials[
            (df_credentials['correo'] == mail_username) & 
            (df_credentials['password'] == password_sfa)
        ]


        if not usuario_valido.empty:
            #agregar info inicio de sesión
            with open(path_df_ingreso , 'a') as f:
                f.write(f'{mail_username}|{fecha_hora_ingreso}\n')
            # Credenciales válidas
            return jsonify({'success': True, 'mensaje': 'Inicio de sesión exitoso.'})
            
        else:
            # Credenciales inválidas
            return jsonify({'success': False, 'mensaje': 'Correo o contraseña incorrectos.'})

    except FileNotFoundError:
        return jsonify({'success': False, 'mensaje': 'Archivo de credenciales no encontrado.'})
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error: {str(e)}'})



@app.route('/agregar_proceso', methods=['POST'])
def agregar_proceso():
    """
    Endpoint para agregar un proceso por cliente usando un archivo de texto.
    """
    data = request.json
    correo = data.get("correo")
    numero_de_radicado = data.get("numero_de_radicado")

    if not correo or not numero_de_radicado:
        return jsonify({"success": False, "message": "Correo y número de radicado son obligatorios."})
    
    if not len(numero_de_radicado) == 23:
        return jsonify({"success": False, "message": "El número de radicado debe tener 23 dígitos."})
    
    # Verificar si el archivo existe y leer su contenido
    registros_existentes = set()
    if os.path.exists(path_archivo_procesos_por_cliente):
        with open(path_archivo_procesos_por_cliente , "r") as archivo:
            registros_existentes = {line.strip() for line in archivo if line.strip()}
    
    # Formatear el registro como "correo|numero_de_radicado"
    nuevo_registro = f"{correo}|{numero_de_radicado}"
    
    if nuevo_registro in registros_existentes:
        return jsonify({"success": False, "message": f"El proceso con el número de radicado {numero_de_radicado} ya está registrado para el correo {correo}."})
    else:
        # Agregar el nuevo registro al archivo
        with open(path_archivo_procesos_por_cliente, "a") as archivo:
            archivo.write(nuevo_registro + "\n")
        return jsonify({"success": True, "message": f"El proceso con el número de radicado {numero_de_radicado} ha sido AGREGADO exitosamente para el correo {correo}."})

@app.route('/eliminar_proceso', methods=['POST'])
def eliminar_proceso():
    """
    Endpoint para eliminar un número de radicado asociado a un correo en el archivo de texto.
    """
    data = request.json
    correo = data.get("correo")
    numero_de_radicado = data.get("numero_de_radicado")

    if not correo or not numero_de_radicado:
        return jsonify({"success": False, "message": "Correo y número de radicado son obligatorios."})

    # Leer los registros existentes
    if not os.path.exists(path_archivo_procesos_por_cliente ):
        return jsonify({"success": False, "message": "El archivo no existe, no hay registros para eliminar."})

    registros_actualizados = []
    registro_eliminado = False

    with open(path_archivo_procesos_por_cliente, "r") as archivo:
        for line in archivo:
            registro = line.strip()
            if registro == f"{correo}|{numero_de_radicado}":
                registro_eliminado = True
            else:
                registros_actualizados.append(registro)

    # Si no se encontró el registro, devolver un mensaje de error
    if not registro_eliminado:
        return jsonify({"success": False, "message": f"No se encontró el proceso con el número de radicado {numero_de_radicado} para el correo {correo}."})

    # Escribir los registros actualizados al archivo
    with open(path_archivo_procesos_por_cliente, "w") as archivo:
        for registro in registros_actualizados:
            archivo.write(registro + "\n")

    return jsonify({"success": True, "message": f"El proceso con el número de radicado {numero_de_radicado} ha sido ELIMINADO exitosamente para el correo {correo}."})

@app.route('/buscar_proceso', methods=['POST'])
def buscar_proceso():
    """
    Endpoint para buscar un número de radicado asociado a un correo en el archivo de texto.
    """
    data = request.json
    correo = data.get("correo")
    numero_de_radicado = data.get("numero_de_radicado")

    if not correo or not numero_de_radicado:
        return jsonify({"success": False, "message": "Correo y número de radicado son obligatorios."})

    # Leer los registros existentes
    if not os.path.exists(path_archivo_procesos_por_cliente):
        return jsonify({"success": False, "message": "El archivo no existe, no se puede realizar la búsqueda."})

    with open(path_archivo_procesos_por_cliente, "r") as archivo:
        for line in archivo:
            registro = line.strip()
            if registro == f"{correo}|{numero_de_radicado}":
                return jsonify({"success": True, "message": f"ENCONTRADO: El número de radicado {numero_de_radicado} ya está en la base de datos para el correo {correo}."})

    return jsonify({"success": False, "message": f"NO EXISTE: El número de radicado {numero_de_radicado} no está registrado para el correo {correo}."})

@app.route('/listar_procesos', methods=['GET'])
def listar_procesos():
    """
    Endpoint para listar los procesos asociados a un correo en el archivo de texto.
    """
    correo = request.args.get('correo')  # Obtener el correo desde los parámetros de la URL

    if not correo:
        return jsonify({"success": False, "message": "Correo es obligatorio."})


    if not os.path.exists(path_archivo_procesos_por_cliente):
        return jsonify({"success": False, "message": "El archivo no existe."})

    procesos = []
    with open(path_archivo_procesos_por_cliente, "r") as archivo:
        for line in archivo:
            registro = line.strip()
            registro_correo, numero_de_radicado = registro.split('|')
            if registro_correo == correo:
                procesos.append(numero_de_radicado)

    if not procesos:
        return jsonify({"success": False, "message": "No hay procesos asociados a este correo."})

    print(procesos)
    return jsonify({"success": True, "procesos": procesos})


@app.route('/generar_reporte', methods=['POST'])
def generar_reporte():
    data = request.json
    correo = data.get("correo")
    
    try:
        ruta_rscript_exe = "C:/Program Files/R/R-4.4.2/bin/Rscript.exe" 
        # Ruta del script de R
        script_path = "C:/Users/USUARIO/Juan Carlos/Software San Francisco de Asis/software_consulta/SENA_informe_consulta_de_procesos.R"
        
        # Ejecutar el script R
        print("Ejecutando script R...")
        result = subprocess.run(
            [ruta_rscript_exe, script_path],  # Llama al ejecutable Rscript
            capture_output=True,
            text=True
        )
        
        # Log de salida y errores
        #print("Salida del script R:", result.stdout)
        #print("Errores del script R:", result.stderr)

        # Verificar si el script se ejecutó correctamente
        if result.returncode != 0:
            return jsonify({"success": False, "message": "Error al ejecutar el script: " + result.stderr})
        
        # Construir la ruta del archivo generado por el script
        path_archivo_excel = f"C:/Users/USUARIO/Juan Carlos/Software San Francisco de Asis/pagina_web/consulta_automatica_procesos_judiciales/back_end/data_base/resultados/consulta_procesos_{correo}.xlsx"
        
        # Verificar si el archivo se generó
        if not os.path.exists(path_archivo_excel):
            return jsonify({"success": False, "message": "El archivo Excel no se generó."})

        # Leer el archivo Excel en memoria
        output = BytesIO()
        with open(path_archivo_excel, "rb") as f:
            output.write(f.read())
            contenido = f.read()
        
        output.seek(0)
        
        # Verificar el tamaño del archivo cargado
        print("Tamaño del archivo original:", os.path.getsize(path_archivo_excel))
        print("Tamaño del archivo cargado en BytesIO:", len(contenido))
        
        # Enviar el archivo Excel como respuesta
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"reporte_generado_{correo}.xlsx"
        )
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})



@app.route('/cargar_varios_procesos', methods=['POST'])
def cargar_varios_procesos():
    try:
        # Obtener el archivo cargado y el correo asociado
        archivo = request.files['archivo']
        correo = request.form.get('correo')  # Obtener correo del formulario

        # Leer el contenido del archivo .txt
        contenido = archivo.read().decode('utf-8').splitlines()

        # Crear el DataFrame para leer los procesos existentes si ya existe el archivo
        # Leer el archivo existente en un DataFrame
        df = pd.read_csv(path_archivo_procesos_por_cliente, sep="|", header=None, names=["correo", "numero_de_radicado"])

        # Crear un conjunto con los radicados ya existentes
        radicados_existentes = set(df['numero_de_radicado'].values)

        # Procesar cada radicado en el archivo cargado
        new_entries = []
        for radicado in contenido:
            # Verificar si el radicado tiene 20 dígitos y es numérico
            if len(radicado) == 23 and radicado.isdigit():
                # Verificar si el radicado ya existe para ese correo
                if radicado not in radicados_existentes:
                    new_entries.append([correo, radicado])
                    radicados_existentes.add(radicado)  # Agregar a los radicados existentes
            else:
                print(f"Radicado inválido: {radicado}")

        # Si hay nuevos radicados, agregarlo al DataFrame
        if new_entries:
            new_df = pd.DataFrame(new_entries, columns=["correo", "numero_de_radicado"])
            df = pd.concat([df, new_df], ignore_index=True)

            # Guardar el DataFrame actualizado en el archivo de texto
            df.to_csv(path_archivo_procesos_por_cliente, sep="|", header=False, index=False)

        return jsonify({"success": True, "message": "Procesos cargados correctamente."})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
@app.route('/upload_file_scraping', methods=['POST'])
def upload_file_scraping():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Ruta personalizada para guardar el archivo
    save_path = r"C:\Users\USUARIO\Juan Carlos\Software San Francisco de Asis\pagina_web\consulta_automatica_procesos_judiciales\back_end\data_base\6consulta_rama_judicial_diaria.txt"
    file.save(save_path)  # Guarda el archivo en la ruta especificada
    return 'File uploaded successfully', 200


if __name__ == "__main__":
    app.run(debug=True)
