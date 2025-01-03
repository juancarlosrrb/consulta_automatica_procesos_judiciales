# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 12:14:22 2024

@author: USUARIO
"""

####sevidor local
import random
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for
import os
from flask_cors import CORS  # Importa CORS
import pandas as pd
from datetime import datetime
import subprocess
from io import BytesIO
import sqlalchemy 
from sqlalchemy import create_engine, Table, Column, MetaData, String, text
import psycopg2
from flask import jsonify, request, send_file
from io import BytesIO
import calendar
import openpyxl

app = Flask(__name__, 
            static_folder='../frontend/site/static',  # Configura la carpeta estática
            template_folder='../frontend/site/template')

# Habilita CORS para todas las rutas
#CORS(app)
# Configuración de CORS: permitir solicitudes de tu frontend
#CORS(app, resources={r"/listar_procesos": {"origins": "http://localhost:3000"}})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/seguimiento_procesos_judiciales')
def seguimiento():
    #para futuras ocasiones investigar lo de session de flask
    #para verificar el logeo
    #if 'correo' not in session:  # Verifica si el usuario no está autenticado
    #    return redirect(url_for('login'))  # Redirige al login si no está autenticado
    return render_template('seguimiento_procesos_judiciales.html')


DATABASE_URL = "postgresql://db_san_francisco_asis_user:ypEDAt8FtqgFMfNbEuLJUCa3A7Amp9jG@dpg-ctpjl68gph6c73df3c3g-a.oregon-postgres.render.com/db_san_francisco_asis"

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)


# Función para leer el archivo de credenciales y verificar si el correo existe
#path_data_base = "C:/Users/USUARIO/Juan Carlos/Software San Francisco de Asis/pagina_web/consulta_automatica_procesos_judiciales/back_end/data_base"
#path_df_token = os.path.join(path_data_base, "1token.txt")
#path_df_credentials = os.path.join(path_data_base, "2credentials_db.txt")
#path_df_ingreso = os.path.join(path_data_base, "5ingreso_plataforma.txt")
#path_archivo_procesos_por_cliente = os.path.join(path_data_base, "3procesos_por_cliente.txt")

table_name_credentials = "2credentials_db"
table_name_tokens = "1token"
table_name_ingreso_plataforma = "5ingreso_plataforma"
table_name_procesos_por_cliente = "3procesos_por_cliente"
table_name_info_n_radicados = "4consulta_n_radicados"
table_name_consulta_diaria = "6consulta_rama_judicial_diaria"

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
        
    try:
            # Lee el archivo como un DataFrame con encabezados
            with engine.connect() as connection:
                df = pd.read_sql_table(table_name_credentials, con=connection)
            
            # Verifica si la columna 'correo' existe y si el correo está en ella
            if 'correo' in df.columns:
                return mail_username in df['correo'].values
            else:
                print("La columna 'correo' no se encuentra en el archivo.")
                return False
    except Exception as e:
            print(f"Error al leer o procesar el archivo: {e}")
            return False



# Función para generar un código de verificación de 4 dígitos
def generar_codigo_verificacion(mail_username):
    """
    Genera un código de verificación de 4 dígitos y lo guarda/actualiza en una tabla PostgreSQL.

    Args:
        mail_username (str): Correo electrónico del usuario.
        engine: Objeto SQLAlchemy Engine conectado a la base de datos.
        table_name_credentials (str): Nombre de la tabla en PostgreSQL.
    
    Returns:
        str: Código de verificación generado.
    """
    codigo_email = str(random.randint(1000, 9999))

    # Conectar a la base de datos
    with engine.connect() as connection:
        # Leer la tabla en un DataFrame
        df = pd.read_sql_table(table_name_tokens, con=connection)

        # Verificar si el correo ya existe
        if mail_username in df['correo'].values:
            # Actualizar el token para el correo existente
            query = text(f"""
                UPDATE "{table_name_tokens}"
                SET token = '{codigo_email}'
                WHERE correo = '{mail_username}';
            """)
        else:
            # Insertar un nuevo registro para el correo
            query = text(f"""
                INSERT INTO "{table_name_tokens}" (correo, token)
                VALUES (:correo, :token);
            """)
        
        # Ejecutar la consulta
        connection.execute(query, {"correo": mail_username, "token": codigo_email})
        connection.commit()

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

    try:
        # Cargar la tabla de tokens en un DataFrame
        with engine.connect() as connection:
            df_tokens = pd.read_sql_table('table_name_tokens', con=connection)
    except Exception as e:
        return jsonify({'mensaje': f'Error al acceder a la tabla de tokens: {str(e)}'})

    # Verificar si el correo y el código coinciden
    user_token = df_tokens[df_tokens['correo'] == mail_username]['codigo'].values

    if len(user_token) > 0 and str(user_token[0]) == str(codigo_ingresado):
        try:
            # Agregar el correo y la contraseña a la tabla de credenciales
            with engine.connect() as connection:
                new_entry = pd.DataFrame({
                    'correo': [mail_username],
                    'password': [password_sfa],
                    'fecha_hora_registro': [fecha_hora_registro]
                })
                new_entry.to_sql('table_name_credentials', con=connection, if_exists='append', index=False)

            # Eliminar el token del usuario de la tabla de tokens
            with engine.connect() as connection:
                query = text(f'DELETE FROM "{table_name_tokens}" WHERE correo = :correo')
                connection.execute(query, {"correo": mail_username})
                connection.commit()
                
            return jsonify({'mensaje': 'Registro exitoso, puedes iniciar sesión ahora.'})
        except Exception as e:
            return jsonify({'mensaje': f'Error al registrar el usuario: {str(e)}'})

    # Si no se encuentra el correo o el código no coincide
    return jsonify({'mensaje': 'El código es incorrecto. Intenta nuevamente.'})

@app.route('/login', methods=['POST'])
def correo_login():
    data = request.json
    mail_username = data.get('mail_username')
    password_sfa = data.get('password_sfa')
    
    # Obtener la fecha y hora actual en el formato deseado
    fecha_hora_ingreso = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Verificar si las credenciales existen en la base de datos
        with engine.connect() as connection:
            # Buscar las credenciales del usuario
            query = text(f"""
                SELECT * FROM "{table_name_credentials}"
                WHERE correo = :correo AND password = :password
            """)
            result = connection.execute(query, {"correo": mail_username, "password": password_sfa})
            usuario_valido = result.fetchone()  # Obtener el primer resultado

            if usuario_valido:
                # Si las credenciales son válidas, agregar información del inicio de sesión a la base de datos
                insert_query = text(f"""
                    INSERT INTO "{table_name_ingreso_plataforma}" (correo, fecha_hora_ingreso)
                    VALUES (:correo, :fecha_hora_ingreso)
                """)
                connection.execute(insert_query, {"correo": mail_username, "fecha_hora_ingreso": fecha_hora_ingreso})
                connection.commit()
                # Guardar sesión del usuario (o generar un token)
                #session['correo'] = mail_username  # Guardar en sesión
 
                # Credenciales válidas
                #return jsonify({'success': True, 'mensaje': 'Inicio de sesión exitoso.'})
                # Login exitoso, redirige al dashboard
                # Enviar respuesta JSON con éxito y la URL de redirección
                # Supongamos que la autenticación es exitosa
                base_url = "http://localhost:3000/frontend/site/template"
                redirect_url = f"{base_url}/seguimiento_procesos_judiciales.html"
                return jsonify({'success': True, 'redirect_url': redirect_url})
                #return jsonify({'success': True, 'redirect_url': '/seguimiento_procesos_judiciales'})

            else:
                # Credenciales inválidas
                return jsonify({'success': False, 'mensaje': 'Correo o contraseña incorrectos.'})

    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error: {str(e)}'})


@app.route('/agregar_proceso', methods=['POST'])
def agregar_proceso():
    """
    Endpoint para agregar un proceso por cliente usando base de datos con SQLAlchemy y engine.
    """
    data = request.json
    correo = data.get("correo")
    numero_de_radicado = data.get("numero_de_radicado")

    if not correo or not numero_de_radicado:
        return jsonify({"success": False, "message": "Correo y número de radicado son obligatorios."})
    
    if not len(numero_de_radicado) == 23:
        return jsonify({"success": False, "message": "El número de radicado debe tener 23 dígitos."})

    try:
        # Crear una nueva sesión
        with engine.connect() as conn:
            # Verificar si el proceso ya está registrado en la base de datos
            query = text(f"""SELECT 1 
                         FROM "{table_name_procesos_por_cliente}" 
                         WHERE correo = :correo AND numero_de_radicado = :numero_de_radicado""")
            result = conn.execute(query, {'correo': correo, 'numero_de_radicado': numero_de_radicado}).fetchone()

            if result:
                return jsonify({"success": False, "message": f"El proceso con el número de radicado {numero_de_radicado} ya está registrado para el correo {correo}."})

            # Insertar el nuevo proceso en la base de datos
            insert_query = text(f"""INSERT INTO "{table_name_procesos_por_cliente}" (correo, numero_de_radicado) 
            VALUES (:correo, :numero_de_radicado)
            """)
            conn.execute(insert_query, {'correo': correo, 'numero_de_radicado': numero_de_radicado})

            # Confirmar los cambios con commit
            conn.commit()

        return jsonify({"success": True, "message": f"El proceso con el número de radicado {numero_de_radicado} ha sido AGREGADO exitosamente para el correo {correo}."})

    except Exception as e:
        # En caso de error al interactuar con la base de datos
        return jsonify({"success": False, "message": f"Hubo un error al agregar el proceso: {str(e)}"})

@app.route('/eliminar_proceso', methods=['POST'])
def eliminar_proceso():
    """
    Endpoint para eliminar un número de radicado asociado a un correo en la base de datos.
    """
    data = request.json
    correo = data.get("correo")
    numero_de_radicado = data.get("numero_de_radicado")

    if not correo or not numero_de_radicado:
        return jsonify({"success": False, "message": "Correo y número de radicado son obligatorios."})

    try:
        # Crear una nueva sesión
        with engine.connect() as conn:
            # Verificar si el proceso existe en la base de datos
            query = text(f"""SELECT 1 
                         FROM "{table_name_procesos_por_cliente}" 
                WHERE correo = :correo AND numero_de_radicado = :numero_de_radicado
            """)
            result = conn.execute(query, {'correo': correo, 'numero_de_radicado': numero_de_radicado}).fetchone()

            if not result:
                return jsonify({"success": False, "message": f"No se encontró el proceso con el número de radicado {numero_de_radicado} para el correo {correo}."})

            # Eliminar el proceso de la base de datos
            delete_query = text(f"""DELETE FROM "{table_name_procesos_por_cliente}"
                WHERE correo = :correo AND numero_de_radicado = :numero_de_radicado
            """)
            conn.execute(delete_query, {'correo': correo, 'numero_de_radicado': numero_de_radicado})

            # Confirmar los cambios con commit
            conn.commit()

        return jsonify({"success": True, "message": f"El proceso con el número de radicado {numero_de_radicado} ha sido ELIMINADO exitosamente para el correo {correo}."})

    except Exception as e:
        # En caso de error al interactuar con la base de datos
        return jsonify({"success": False, "message": f"Hubo un error al eliminar el proceso: {str(e)}"})


@app.route('/buscar_proceso', methods=['POST'])
def buscar_proceso():
    """
    Endpoint para buscar un número de radicado asociado a un correo en la base de datos.
    """
    data = request.json
    correo = data.get("correo")
    numero_de_radicado = data.get("numero_de_radicado")

    if not correo or not numero_de_radicado:
        return jsonify({"success": False, "message": "Correo y número de radicado son obligatorios."})

    try:
        # Crear una nueva sesión
        with engine.connect() as conn:
            # Verificar si el proceso existe en la base de datos
            query = text(f"""SELECT 1 FROM "{table_name_procesos_por_cliente}"
                WHERE correo = :correo AND numero_de_radicado = :numero_de_radicado
            """)
            result = conn.execute(query, {'correo': correo, 'numero_de_radicado': numero_de_radicado}).fetchone()

            if result:
                return jsonify({"success": True, "message": f"ENCONTRADO: El número de radicado {numero_de_radicado} ya está en la base de datos para el correo {correo}."})
            else:
                return jsonify({"success": False, "message": f"NO EXISTE: El número de radicado {numero_de_radicado} no está registrado para el correo {correo}."})

    except Exception as e:
        # En caso de error al interactuar con la base de datos
        return jsonify({"success": False, "message": f"Hubo un error al buscar el proceso: {str(e)}"})

@app.route('/listar_procesos', methods=['GET'])
def listar_procesos():
    """
    Endpoint para listar los procesos asociados a un correo en la base de datos PostgreSQL.
    """
    #print("entro a listar procesos")
    correo = request.args.get('correo')  # Obtener el correo desde los parámetros de la URL

    #print(correo)
    if not correo:
        return jsonify({"success": False, "message": "Correo es obligatorio."})

    try:
        with engine.connect() as connection:
            query = text(f"""
                SELECT numero_de_radicado 
                FROM "{table_name_procesos_por_cliente}"
                WHERE correo = :correo
            """)
            #print(query)
            result = connection.execute(query, {"correo": correo}).fetchall()

            procesos = [row[0] for row in result]

            if not procesos:
                return jsonify({"success": False, "message": "No hay procesos asociados a este correo."})

        #jsonify({"success": True, "procesos": "ya_casi"})#
        return jsonify({"success": True, "procesos": procesos})

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})


@app.route('/generar_reporte', methods=['POST'])
def generar_reporte():
    """
    Endpoint para generar un reporte en Excel con múltiples pestañas derivadas de una única consulta SQL.
    """
    data = request.json
    correo = data.get("correo")

    if not correo:
        return jsonify({"success": False, "message": "Correo es obligatorio."})

    try:
        # Ejecutar consulta SQL para obtener todos los datos necesarios
        with engine.connect() as conn:
            query = text(f"""SELECT 
                    pc.correo, 
                    pc.numero_de_radicado, 
                    sfa.fecha_ult_actuacion, 
                    info_radicados.ciudad, 
                    info_radicados.entidad_o_especialidad
                FROM public."{table_name_procesos_por_cliente}" pc
                LEFT JOIN public."{table_name_consulta_diaria}" sfa
                    ON pc.numero_de_radicado = sfa.numero_de_radicado
                LEFT JOIN public."{table_name_info_n_radicados}" info_radicados
                    ON pc.numero_de_radicado = info_radicados.numero_de_radicado
                WHERE pc.correo = :correo
            """)
            df = pd.read_sql(query, conn, params={"correo": correo})

        # Convertir fecha_ult_actuacion al formato datetime
        df["fecha_ult_actuacion"] = pd.to_datetime(df["fecha_ult_actuacion"], errors="coerce", format="%d %b %Y")

        # Crear las hojas del reporte
        total_procesos_SOLICITADOS = df[["correo", "numero_de_radicado"]].drop_duplicates()
        total_procesos_buscados = df.dropna(subset=["fecha_ult_actuacion"])
        procesos_NO_BUSCADOS = df[df["fecha_ult_actuacion"].isna()]
        procesos_no_encontrados = df[df["fecha_ult_actuacion"] == "no_encontro_informacion"]
        procesos_SI_encontrados = df[
            (df["fecha_ult_actuacion"].notna()) & 
            (df["fecha_ult_actuacion"] != "no_encontro_informacion")]
        procesos_con_actuacion_este_mes = total_procesos_buscados[
            total_procesos_buscados["fecha_ult_actuacion"] >= datetime.now().replace(day=1)
        ]
        procesos_actuacion_esta_semana = total_procesos_buscados[
            total_procesos_buscados["fecha_ult_actuacion"] >= datetime.now() - pd.Timedelta(days=datetime.now().weekday())
        ]

        # Garantizar columnas si los DataFrames están vacíos
        columnas = {
            "total_procesos_SOLICITADOS": ["correo", "numero_de_radicado"],
            "total_procesos_buscados": df.columns.tolist(),
            "procesos_NO_BUSCADOS": df.columns.tolist(),
            "procesos_no_encontrados": df.columns.tolist(),
            "procesos_SI_encontrados": df.columns.tolist(),
            "procesos_con_actuacion_este_mes": df.columns.tolist(),
            "procesos_actuacion_esta_semana": df.columns.tolist(),
        }
        # Diccionario con los DataFrames por hoja
        hojas = {
            nombre: df_hoja if not df_hoja.empty else pd.DataFrame(columns=columnas[nombre])
            for nombre, df_hoja in {
                "total_procesos_SOLICITADOS": total_procesos_SOLICITADOS,
                "total_procesos_buscados": total_procesos_buscados,
                "procesos_NO_BUSCADOS": procesos_NO_BUSCADOS,
                "procesos_no_encontrados": procesos_no_encontrados,
                "procesos_SI_encontrados": procesos_SI_encontrados,
                "procesos_con_actuacion_este_mes": procesos_con_actuacion_este_mes,
                "procesos_actuacion_esta_semana": procesos_actuacion_esta_semana,
            }.items()
        }
        # Crear el archivo Excel
        output = BytesIO()
        #with pd.ExcelWriter(output, engine='openpyxl') as writer:
        #    for sheet_name, df_hoja in hojas.items():
        #        df_hoja.to_excel(writer, index=False, sheet_name=sheet_name)
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet_name, df_hoja in hojas.items():
                # Escribir el DataFrame en la hoja
                df_hoja.to_excel(writer, index=False, sheet_name=sheet_name)
                
                # Ajustar automáticamente el ancho de las columnas
                worksheet = writer.sheets[sheet_name]
                for col_idx, column in enumerate(df_hoja.columns, start=1):
                    max_length = max(
                        df_hoja[column].astype(str).map(len).max(),  # Longitud máxima del contenido
                        len(column)  # Longitud del nombre de la columna
                    )
                    worksheet.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = max_length + 2

        output.seek(0)

        # Enviar el archivo Excel como respuesta
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"reporte_generado_{correo}.xlsx"
        )

    except Exception as e:
        return jsonify({"success": False, "message": f"Error al generar el reporte: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=False)
