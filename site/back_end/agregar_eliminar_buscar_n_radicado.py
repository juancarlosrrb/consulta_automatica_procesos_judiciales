# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 12:03:25 2024

@author: USUARIO
"""

import pandas as pd

# Archivos simulados
archivo_txt1 = "df_numero_radicados.txt"

# Función para agregar un número de radicado
def agregar_radicado(numero_radicado, correo):
    df = pd.read_csv(archivo_txt1, sep=",", names=["numero_radicado", "correo"], dtype=str)
    if str(numero_radicado) in df["numero_radicado"].values:
        return "El número de radicado ya existe."
    else:
        df = df.append({"numero_radicado": str(numero_radicado), "correo": correo}, ignore_index=True)
        df.to_csv(archivo_txt1, sep=",", index=False, header=False)
        return "Número de radicado agregado correctamente."

# Función para eliminar un número de radicado
def eliminar_radicado(numero_radicado):
    df = pd.read_csv(archivo_txt1, sep=",", names=["numero_radicado", "correo"], dtype=str)
    if str(numero_radicado) in df["numero_radicado"].values:
        df = df[df["numero_radicado"] != str(numero_radicado)]
        df.to_csv(archivo_txt1, sep=",", index=False, header=False)
        return "Número de radicado eliminado correctamente."
    else:
        return "Número de radicado no encontrado."

# Función para buscar un número de radicado
def buscar_radicado(numero_radicado):
    df = pd.read_csv(archivo_txt1, sep=",", names=["numero_radicado", "correo"], dtype=str)
    if str(numero_radicado) in df["numero_radicado"].values:
        return "Número de radicado encontrado en tu lista."
    else:
        return "Este proceso no existe."

# Prueba local
correo_cliente = "cliente@email.com"
print(agregar_radicado("123456789", correo_cliente))
print(eliminar_radicado("123456789"))
print(buscar_radicado("123456789"))
