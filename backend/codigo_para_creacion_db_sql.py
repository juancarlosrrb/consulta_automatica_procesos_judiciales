# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 10:46:45 2024

@author: USUARIO
"""

import os
import pandas as pd
from sqlalchemy import create_engine

from sqlalchemy import create_engine

DATABASE_URL = "postgresql://db_san_francisco_asis_user:ypEDAt8FtqgFMfNbEuLJUCa3A7Amp9jG@dpg-ctpjl68gph6c73df3c3g-a.oregon-postgres.render.com/db_san_francisco_asis"

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Verificar la conexión
try:
    with engine.connect() as connection:
        print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar: {e}")


# Ruta de los archivos txt
ruta_txt = r"C:\Users\USUARIO\Juan Carlos\Software San Francisco de Asis\pagina_web\consulta_automatica_procesos_judiciales\backend\data_base"

# Leer todos los archivos .txt en la ruta
for archivo in os.listdir(ruta_txt):
    if archivo.endswith(".txt"):
        # Obtener el nombre del archivo sin extensión para usarlo como nombre de tabla
        nombre_tabla = os.path.splitext(archivo)[0]

        # Leer el archivo como DataFrame
        ruta_completa = os.path.join(ruta_txt, archivo)
        df = pd.read_csv(ruta_completa, delimiter='|', engine="python")  # Cambia `sep="\t"` según tu formato

        # Crear la tabla en la base de datos e insertar los datos
        df.to_sql(nombre_tabla, engine, if_exists="replace", index=False)
        print(f"Tabla '{nombre_tabla}' creada exitosamente con {len(df)} registros.")


#código para leer alguna tabla
# Leer la tabla con pandas
table_name = "2credentials_db"
try:
    with engine.connect() as connection:
        df = pd.read_sql_table(table_name, con=connection)
        print("Datos de la tabla:")
        print(df.head())  # Muestra las primeras filas de la tabla
except Exception as e:
    print(f"Error al leer la tabla: {e}")