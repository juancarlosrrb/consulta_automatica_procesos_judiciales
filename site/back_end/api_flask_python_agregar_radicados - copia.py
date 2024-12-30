# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 12:14:22 2024

@author: USUARIO
"""

####API FLASK
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Simulación del archivo TXT
ARCHIVO_TXT1 = "df_numero_radicados.txt"


# Simulación de autenticación
@app.route('/correo_login', methods=['POST'])
def enviar_correo_login():
    datos = request.json
    correo = datos['mail_username']
    password = datos['password_sfa']
    
    # Simulación de usuario válido
    if correo == 'cliente@email.com' and password == '1234':
        return jsonify({"mensaje": "Login exitoso", "correo": correo})
    return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401

# Ruta: Agregar número de radicado
@app.route('/agregar', methods=['POST'])
def agregar_numero_radicado():
    data = request.json
    numero_radicado = data.get("numero_radicado")
    correo = data.get("correo")

    df = pd.read_csv(ARCHIVO_TXT1, sep=",", names=["numero_radicado", "correo"], dtype=str)
    if str(numero_radicado) in df["numero_radicado"].values:
        return jsonify({"mensaje": "El número de radicado ya existe."}), 400
    else:
        df = df.append({"numero_radicado": str(numero_radicado), "correo": correo}, ignore_index=True)
        df.to_csv(ARCHIVO_TXT1, sep=",", index=False, header=False)
        return jsonify({"mensaje": "Número de radicado agregado correctamente."}), 200

# Ruta: Eliminar número de radicado
@app.route('/eliminar', methods=['POST'])
def eliminar_radicado():
    data = request.json
    numero_radicado = data.get("numero_radicado")

    df = pd.read_csv(ARCHIVO_TXT1, sep=",", names=["numero_radicado", "correo"], dtype=str)
    if str(numero_radicado) in df["numero_radicado"].values:
        df = df[df["numero_radicado"] != str(numero_radicado)]
        df.to_csv(ARCHIVO_TXT1, sep=",", index=False, header=False)
        return jsonify({"mensaje": "Número de radicado eliminado correctamente."}), 200
    else:
        return jsonify({"mensaje": "Número de radicado no encontrado."}), 400

# Ruta: Buscar número de radicado
@app.route('/buscar', methods=['GET'])
def buscar_radicado():
    numero_radicado = request.args.get("numero_radicado")
    df = pd.read_csv(ARCHIVO_TXT1, sep=",", names=["numero_radicado", "correo"], dtype=str)

    if str(numero_radicado) in df["numero_radicado"].values:
        return jsonify({"mensaje": "Número de radicado encontrado en tu lista."}), 200
    else:
        return jsonify({"mensaje": "Este proceso no existe."}), 404

if __name__ == '__main__':
    app.run(debug=True)
